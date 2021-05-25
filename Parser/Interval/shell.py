from main import run

while True:
    text = input('basic > ')

    if text == "q":
        print("Exiting...")
        break

    result, error = run('<stdin>', text)

    if error:
        print(error.as_string())

    else:
        print(result)