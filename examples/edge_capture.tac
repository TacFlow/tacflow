flow edge_capture {
    // Trigger camera on a remote IoT edge device
    // Demonstrates: edge device routing, binary output handling, push notification

    trigger: on_command "capture"

    step locate_device {
        description: "Find the nearest available edge device with a camera"
        input: @user location_hint
        action: edge.find_device("camera", "{{location_hint}}")
        output: @verified device_id
    }

    step verify_device {
        description: "Check device is online and camera is responsive"
        input: @verified device_id
        action: edge.ping("{{device_id}}")
        output: @verified device_status
    }

    step capture_photo {
        description: "Capture photo from edge device camera"
        input: @verified device_id, @verified device_status
        condition: "{{device_status}} == online"
        action: edge.camera_capture("{{device_id}}", quality=12)
        output: @verified photo_path
    }

    step analyze_image {
        description: "Run OCR and object detection on captured image"
        input: @verified photo_path
        action: vision.analyze("{{photo_path}}", ["ocr", "objects"])
        output: @inferred analysis
    }

    step notify {
        description: "Send photo and analysis to user"
        input: @verified photo_path, @inferred analysis
        action: push.send(
            title="Edge Capture Complete",
            message="Photo captured from device {{device_id}}",
            attachment="{{photo_path}}",
            priority=high
        )
    }
}
