import argparse
import json
import os
import requests
from bs4 import BeautifulSoup


def get_html_content(url):
    return requests.get(url).content


def get_beautiful_soup_object(html_content, parser="html.parser"):
    return BeautifulSoup(html_content, parser)


def get_table_element(bs, attrs={"class": "row-hover"}):
    return bs.find(attrs=attrs)


def get_song_objects_in_table(
        table_element, even_rows_attrs={"class": "even"}, odd_rows_attrs={"class": "odd"}, elem_with_info="a",
        first_song=1, last_song=694
    ):
    even_rows = table_element.find_all(attrs=even_rows_attrs)
    odd_rows = table_element.find_all(attrs=odd_rows_attrs)
    all_rows = [i.find(elem_with_info) for i in even_rows + odd_rows]
    urls = [(int(i["href"].split("/")[-2][:3]), i.text, i["href"]) for i in all_rows]
    urls.sort(key=lambda x: x[0])

    return urls[first_song - 1 : last_song]


def get_song_text(bs, title, elem_with_info="td"):
    table_data = bs.find(elem_with_info)
    to_decompose = [table_data.find("iframe"), table_data.find("script")] + table_data.find_all("div")

    while None in to_decompose:
        to_decompose.remove(None)

    [i.decompose() for i in to_decompose]

    paragraphs = table_data.find_all("p")
    song_text = {idx + 1: p.text.split("\n") for idx, p in enumerate(paragraphs)}
    song_text["title"] = title

    return song_text


def get_formatted_song_text(song_text):
    cleaned = {}
    number_of_skipped = 0

    for k, v in song_text.items():
        if k == "title":
            cleaned[k] = v
            continue

        try:
            int(v[0])
            v = v[1:]
        except ValueError:
            if v[0] == "Refrain":
                number_of_skipped += 1
                cleaned["Refrain"] = v[1:]
                continue

        while "" in v:
            v.remove("")
        if len(v) == 0:
            number_of_skipped += 1
            continue

        cleaned[k - number_of_skipped] = v

    formatted = {
        "stanzas": [{
            "number": k,
            "lines": [{
                "number": idx + 1,
                "text": val
            } for idx, val in enumerate(v)]
        } for k, v in cleaned.items() if k != "Refrain" and k != "title"]
    }

    if "Refrain" in cleaned:
        formatted["refrain"] = {
            "lines": [{
                "number": idx + 1,
                "text": val
            } for idx, val in enumerate(cleaned["Refrain"])]
        }

    formatted["title"] = cleaned["title"]

    return formatted


def save_as_json(formatted_song_text, file_path):
    with open(file_path, "w") as f:
        json.dump(formatted_song_text, f)


def main(url, save_dir):
    html_content = get_html_content(url)
    bs = get_beautiful_soup_object(html_content)
    table_element = get_table_element(bs)
    song_objs = get_song_objects_in_table(table_element)
    num_of_songs = len(song_objs)

    for idx, i in enumerate(song_objs):
        song_text = get_song_text(
            get_beautiful_soup_object(
                get_html_content(i[2])
            ), i[1]
        )
        formatted_song_text = get_formatted_song_text(song_text)
        song_number = f"{i[0]}"

        while len(song_number) < 3:
            song_number = f"0{song_number}"

        save_as_json(formatted_song_text, os.path.join(save_dir, f"{song_number}.json"))
        print(f"\r{idx + 1}/{num_of_songs}", end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraper to acquire English hymnals")
    parser.add_argument("-d", "--directory", type=str, help="Directory to save files to")

    args = parser.parse_args()

    if args.directory is None:
        print("[ERROR] Usage is: python en.py -d <dir/path/to/save/files/to/>")
        exit(1)
    elif not os.path.exists(args.directory):
        print("[ERROR] The provided directory path does not exist")
        exit(1)

    main("https://sdahymnals.com/Hymnal/", args.directory)
