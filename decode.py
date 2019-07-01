class Decoder():
    def __init__(self, obfuscated, original, start="!", end=127):
        difference = ord(obfuscated) - ord(original)
        self.start_character= ord(start)
        self.key = abs(difference)
        self.end_character = end

    def original(self, text):
        decoded_text = ""

        for character in reversed(text):
            if character is not " ":
                decoded_character = ord(character) - self.key
                if decoded_character < self.start_character:
                    decoded_character = self.end_character - abs(decoded_character - self.start_character)
                decoded_text = decoded_text + str(chr(decoded_character))
            else:
                decoded_text = decoded_text + character

        return decoded_text

decoder = Decoder("2", "a")