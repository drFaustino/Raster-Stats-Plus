import csv


def stats_to_text(stats):
    return "\n".join(f"{k}: {v}" for k, v in stats.items())


def export_stats_csv(path, stats_dict, delimiter=";"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(["stat", "value"])

        for k, v in stats_dict.items():
            writer.writerow([k, v])
