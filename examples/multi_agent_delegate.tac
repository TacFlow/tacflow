flow multi_agent_delegate {
    // Complex task decomposed across 3 specialized agents
    // Demonstrates: agent routing, swarm consensus, trust validation

    trigger: on_complex_task

    step security_scan {
        description: "Sentinela analyzes the task for security threats"
        agent: sentinela
        input: @user task
        action: security.analyze_threat("{{task}}")
        output: @verified threat_level
    }

    step deep_research {
        description: "Fluxo Criativo performs deep research on the topic"
        agent: fluxo_criativo
        input: @user task
        action: research.deep_dive("{{task}}")
        output: @inferred research_data
    }

    step validate_research {
        description: "Cross-validate research findings against trusted sources"
        input: @inferred research_data
        action: trust.validate_source("{{research_data}}")
        output: @verified validated_research
    }

    step swarm_consensus {
        description: "Agents vote on whether it's safe to proceed"
        input: @verified threat_level, @verified validated_research
        action: swarm.consensus("safe_to_execute", [sentinela, fluxo_criativo, r1])
        trust: require @swarm for execution
        output: @swarm consensus_decision
    }

    step conditional_execute {
        description: "Execute only if swarm consensus approves"
        input: @swarm consensus_decision, @verified validated_research
        condition: "{{consensus_decision}} == approved"
        action: task.execute("{{validated_research}}")
        output: @inferred result
    }

    step notify_user {
        description: "Report result with full audit trail"
        input: @inferred result, @swarm consensus_decision
        action: message.send(
            "Task complete.\n" +
            "Result: {{result}}\n" +
            "Decision: {{consensus_decision}}\n" +
            "Agents involved: sentinela, fluxo_criativo, r1"
        )
    }
}
