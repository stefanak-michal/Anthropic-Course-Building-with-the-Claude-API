from utils.ai import send, add_user_message, add_assistant_message

while True:
    try:
        msg = input("\nEnter your message: ")
    except EOFError:
        print("\nNo stdin detected. Exiting.")
        break
    if msg:
        print("\n---\n")
        add_user_message(msg)
        response = send()
        print("\n---\n")
        add_assistant_message(response)
    else:
        break
