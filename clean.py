import inflect
import re
import unidecode
import json
import string

p = inflect.engine()


def printable_only(text: str) -> str:
    """_Removes crap characters that don't play nicely with things like TTS processors._

    Args:
        text (str): _Takes a string that needs to be cleaned._

    Returns:
        str: _Returns only printable characters in the form of a string after creating an iterable that is then rejoined after filtering._
    """
    printable = set(string.printable)
    return "".join(filter(lambda x: x in printable, text))


def raw_list_from_file(text_path: str) -> list:
    """Pulls text from a file and returns it as a list.

    Args:
        text_path (str): The path of the text file.

    Returns:
        list: A list of lines to be cleaned.
    """
    line_list = []

    with open(text_path, "r", encoding="utf-8") as f:
        for line in f:
            line_list.append(line)

    return line_list


def clean_years_l(line_list: list, inf_eng: inflect.engine) -> list:
    """Transforms all years from numberals to words.

    Args:
        line_list (list): _description_
        inf_eng (inflect.engine): _description_

    Returns:
        list: Returns a cleaned list of the line_list argument.
    """
    for idx, line in enumerate(line_list):
        results = re.findall("(\D)(\d{4})(\D)", line)
        for result in results:
            year_change = re.sub(
                "-oh-oh",
                "-hundred",
                re.sub(
                    "oh\s",
                    "oh-",
                    re.sub(
                        ",\s", "-", p.number_to_words(result[1], group=2, zero="oh")
                    ),
                ),
            )
            single_years = [
                "one",
                "two",
                "three",
                "four",
                "five",
                "six",
                "seven",
                "eight",
                "nine",
            ]
            for year in single_years:
                if year_change[:6] == "twenty":
                    year_change = re.sub(
                        f"twenty-oh-{year}", f"two-thousand-and-{year}", year_change
                    )
                else:
                    year_change = re.sub(
                        f"oh-{year}", f"hundred-and-{year}", year_change
                    )
            line_list[idx] = re.sub(result[1], year_change, line_list[idx])
    return line_list


def clean_numbers_l(line_list: list, inf_eng: inflect.engine) -> list:
    """Turns all non-year numbers into words.

    Args:
        line_list (list): _description_
        inf_eng (inflect.engine): _description_

    Returns:
        list: _Returns a cleaned list of the line_list argument._
    """

    for idx, line in enumerate(line_list):
        result = re.findall("(\d+)", line)
        for found_num in result:
            l_found_num = list(found_num)
            l_found_num[0] = inf_eng.number_to_words(l_found_num, andword=" and")
            found_num = tuple(l_found_num)
            repl = f"{found_num[0]}"
            updated_line = re.sub("\d+", repl, line)
            line_list[idx] = unidecode.unidecode(updated_line)
    return line_list


def to_file(text_list: list, dest_path: str) -> None:
    """
    Writes the cleaned text to a file.
    """
    with open(dest_path, "w+", encoding="utf-8") as f:
        for line in text_list:
            f.write(line)


def to_json(text_list: list, dest_path: str) -> None:
    """
    Writes the cleaned text to a json file.
    """

    list_container = {"text_list": []}

    for line in text_list:
        list_container["test_list"].append(line)

    with open(dest_path, "w+", encoding="utf-8") as f:
        json.dump(list_container, f, indent=4)

def clean_titles(text_list:list)->list:
    title_list = []
    title_clean_top = 0
    title_clean_mid = 0
    for idx, line in enumerate(text_list):
        if line.isupper():
            title_list.append(line)
            if len(title_list) == 2:
                title_clean_mid = idx
                title_clean_top = idx-2
            if len(title_list) == 3:
                text_list[idx] = " ".join(title_list)
                title_list = []
                text_list.remove(text_list[title_clean_mid])
                text_list.remove(text_list[title_clean_top])
    return text_list

def last_pass(text_list: str, dest_path: str) -> None:
    """_Cleans the text_list argument of unprintable and unwanted characters then writes it to a file._

    Args:
        text_list (str): _The list of text lines to be cleaned_
        dest_path (str): _The path of the output file including the file name and extension._
    """
    final_lines = []
    for line in text_list:
        line = re.sub("\s+", " ", line)
        line = re.sub("\n", "", line)
        line = re.sub("\r", "", line)
        line = re.sub("\t", "", line)
        line = "".join([line, "\n"])
        final_lines.append(printable_only(line))
    to_file(final_lines, dest_path)


if __name__ == "__main__":

    def main(text_path: str, dest_path: str, inf_eng: inflect.engine):
        """_Cleans the text_path argument and writes it to a file._"""
        last_pass(
            clean_titles(
                clean_numbers_l(
                    clean_years_l(raw_list_from_file(text_path), inf_eng), inf_eng
                ),
            ),
            dest_path,
        )

    main("text_files/origin_text.txt", "text_files/clean.txt", p)
