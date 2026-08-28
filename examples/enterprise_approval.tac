flow enterprise_approval {
    // Multi-step approval workflow with human-in-the-loop checkpoint
    // Demonstrates: human approval gate, trust escalation, compliance logging

    trigger: on_document_review

    step receive_document {
        description: "Receive document and extract metadata"
        input: @user document_id
        action: document.load("{{document_id}}")
        output: @verified document
    }

    step classify_sensitivity {
        description: "Classify document sensitivity level"
        input: @verified document
        action: security.classify("{{document}}")
        output: @verified sensitivity_level
    }

    step auto_review {
        description: "AI-powered initial review (low-sensitivity only)"
        input: @verified document, @verified sensitivity_level
        condition: "{{sensitivity_level}} <= medium"
        action: llm.analyze("Review document: {{document}}. Check for: compliance, errors, missing data")
        output: @inferred review_notes
    }

    step human_approval_gate {
        description: "HUMAN-IN-THE-LOOP — requires explicit approval for any action"
        input: @inferred review_notes, @verified sensitivity_level
        action: approval.request(
            title="Document Review: {{document_id}}",
            context="{{review_notes}}",
            sensitivity="{{sensitivity_level}}",
            required_approvers=["compliance_officer", "team_lead"],
            timeout_hours=24
        )
        trust: require @user for proceed
        output: @user approval_decision
    }

    step conditional_approve {
        description: "Process based on human decision"
        input: @user approval_decision, @verified document
        condition: "{{approval_decision}} == approved"
        action: document.finalize("{{document}}")
        output: @verified finalized_document
    }

    step conditional_reject {
        description: "Handle rejection with feedback"
        input: @user approval_decision, @verified document
        condition: "{{approval_decision}} == rejected"
        action: document.reject("{{document}}", reason="{{approval_decision.reason}}")
        output: @verified rejection_record
    }

    step log_audit {
        description: "Immutable audit trail of entire workflow"
        input: @verified document, @user approval_decision
        action: audit.log(
            event="document_review",
            document_id="{{document_id}}",
            decision="{{approval_decision}}",
            timestamp="{{system.now}}",
            agent_id="{{system.agent_id}}"
        )
        output: @system audit_hash
    }

    step notify_stakeholders {
        description: "Notify all stakeholders of the outcome"
        input: @verified finalized_document, @verified rejection_record, @system audit_hash
        action: message.send(
            to=["compliance@company.com", "requestor@company.com"],
            subject="Document Review Complete: {{document_id}}",
            body="Audit hash: {{audit_hash}}"
        )
    }
}
