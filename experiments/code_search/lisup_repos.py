from experiments.github import get_github_token
from experiments.github.github import GitHub


def main():
    gh = GitHub()
    gh.login("Hiroya-W", get_github_token())
    query = '"Here Be Dragons" in:file language:c'
    res = gh.search_code(query, per_page=10, page=1, text_match=True)
    print(res.url)

    if res.status_code == 200:
        res_json = res.json()
        print("total_count: ", res_json.get("total_count"))
        print("incomplete_results: ", res_json.get("incomplete_results"))
        items = res_json.get("items")
        for item in items:
            repository = item.get("repository").get("full_name")
            text_matches = item.get("text_matches")
            print(repository)
            print(text_matches)
    else:
        print(res.status_code)


if __name__ == "__main__":
    main()
