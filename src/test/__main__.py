from classifier import TypeClassifier

if __name__ == '__main__':
    data = [
        "",
        "abc",
        "123",
        "`const PI = 3.14159`",
        "google.com",
        "https://github.com/microsoft",
        "me@gmail.com",
        "192.168.0.1",
        "https://1.1.1.1",
        "#hashtag",
        "@elonmusk"
    ]
    
    typeClassifier = TypeClassifier()
    classes = typeClassifier.classify(' '.join(data))
    for _class in classes:
        print(f'"{_class.value}" is of type `{_class.type}`')