from robotpt_common_utils import lists
from text_populator.populator import TextPopulator


class Message:

    class Type:
        MULTIPLE_CHOICE = "multiple choice"
        DIRECT_INPUT = "direct input"

    def __init__(
            self,
            content,
            options,
            message_type,
            result_type=str,
            tests=None,
            error_message="Please enter a valid input",
            error_options=('Okay', 'Oops'),
            text_populator=None,
    ):
        if text_populator is not None and type(text_populator) is not TextPopulator:
            raise ValueError
        self._text_populator = text_populator

        if not self._test_markup(content):
            raise ValueError(f"Invalid content: '{content}'")
        self._content = content

        options = lists.make_sure_is_iterable(options)
        if not self._test_markup(options):
            raise ValueError(f"Invalid options: '{options}'")
        self._options = options

        self._message_type = message_type
        self._result_type = result_type

        if tests is not None:
            tests = lists.make_sure_is_iterable(tests)
        self._tests = tests
        self._error_message = error_message
        self._error_options = error_options

    def _test_markup(self, text):

        if self._text_populator is None:
            return True

        if lists.is_iterable(text):
            return all([self._text_populator.test(t) for t in text])
        else:
            return self._text_populator.test(text)

    def _markup(self, text):

        if self._text_populator is None:
            return text

        if lists.is_iterable(text):
            return [self._text_populator.run(t) for t in text]
        else:
            return self._text_populator.run(text)

    @property
    def content(self):
        return self._markup(self._content)

    @property
    def options(self):
        return [self._markup(o) for o in self._options]

    @property
    def message_type(self):
        return self._message_type

    @property
    def result_type(self):
        return self._result_type

    @property
    def tests(self):
        return self._tests

    @property
    def error_message(self):
        return Message(
            content=self._error_message,
            options=self._error_options,
            message_type=Message.Type.MULTIPLE_CHOICE,
            text_populator=self._text_populator
        )


if __name__ == "__main__":

    import os
    from pickled_database import PickledDatabase
    from text_populator.database_populator import DatabasePopulator
    from text_populator.variety_populator import VarietyPopulator

    db_file = 'test_db.pkl'
    db = PickledDatabase(db_file)
    db.create_key_if_not_exists('key1', 1)
    db.create_key_if_not_exists('key2', 'two')
    db.create_key_if_not_exists('no_value_key')
    db.create_key_if_not_exists('user_name', 'Audrow')
    db.create_key_if_not_exists('question_idx', 1)

    my_str = """
{'var': 'greeting'}, {'db': 'user_name'}. 
{'rand': ["What's up", 'How are you', "How's it going"]}?
{'var': 'question', 'index': '{'db': 'question_idx', 'post-op': 'increment'}'}
{'var': '{'var': 'foo'}bar'}
    """

    variation_file = 'variation.csv'
    variation_file_contents = """
Code,Text
greeting,Hi
greeting,Hello
greeting,Hola
question,Do you like green?
question,Do you like dogs?
question,Do you like apples?
question,Do you like me?
foo,foo
foo,fake
foobar,foo-bar
fakebar,fake-bar
    """

    with open(variation_file, 'w', newline='') as csvfile:
        csvfile.write(variation_file_contents.strip())

    import atexit

    atexit.register(lambda: os.remove(db_file))
    atexit.register(lambda: os.remove(variation_file))

    variety_populator_ = VarietyPopulator(variation_file)
    database_populator_ = DatabasePopulator(db_file)

    text_populator = TextPopulator(variety_populator_, database_populator_)

    no_variation_msg = Message(
        content='Here is a question, or is it?',
        options='Not sure',
        message_type=Message.Type.MULTIPLE_CHOICE,
        text_populator=text_populator
    )
    print(no_variation_msg.content)
    print(no_variation_msg.options)

    variation_msg = Message(
        content=my_str,
        options=["{'rand': ['Yes', 'Definitely', 'Ofcourse']}", "{'rand': ['No', 'No way']}"],
        message_type=Message.Type.MULTIPLE_CHOICE,
        text_populator=text_populator
    )
    print(variation_msg.content)
    print(variation_msg.options)