flow hello_agent {
    // Basic greeting flow — demonstrates TAC Language fundamentals
    // Trust Types: @user, @inferred, @system

    trigger: on_message

    step greet {
        description: "Receive user's name and generate a warm greeting"
        input: @user name
        action: llm.generate("Greet {{name}} warmly and ask how you can help")
        output: @inferred greeting
    }

    step respond {
        description: "Send the greeting back to the user"
        input: @inferred greeting
        action: message.send("{{greeting}}")
    }
}
