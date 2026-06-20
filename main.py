from datetime import datetime
from pathlib import Path

import gifos
from zoneinfo import ZoneInfo


BASE_DIR = Path(__file__).resolve().parent
FONT_DIR = BASE_DIR / "gifos" / "fonts"


def first_existing_font(*paths: Path) -> str:
    for path in paths:
        if path.exists():
            return str(path)
    raise FileNotFoundError(
        "No usable font found. Add fonts under gifos/fonts or run through Docker."
    )


SYSTEM_MONO_FONTS = [
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
    Path("/System/Library/Fonts/Menlo.ttc"),
    Path("/Library/Fonts/Menlo.ttc"),
]
SYSTEM_BOLD_MONO_FONTS = [
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    Path("/System/Library/Fonts/Menlo.ttc"),
    Path("/Library/Fonts/Menlo.ttc"),
]

FONT_FILE_LOGO = first_existing_font(
    FONT_DIR / "vtks-blocketo.regular.ttf", *SYSTEM_BOLD_MONO_FONTS
)
FONT_FILE_BITMAP = first_existing_font(FONT_DIR / "gohufont-uni-14.pil", *SYSTEM_MONO_FONTS)
FONT_FILE_ASCII = first_existing_font(FONT_DIR / "NotoMono-Regular.ttf", *SYSTEM_MONO_FONTS)

def main():
    t = gifos.Terminal(795, 490, 15, 15, FONT_FILE_BITMAP, 15)

    t.gen_text("", 1, count=20)
    t.toggle_show_cursor(False)
    year_now = datetime.now(ZoneInfo("America/Panama")).strftime("%Y")
    t.gen_text("GIF_OS Modular BIOS v1.0.11", 1)
    t.gen_text(f"Copyright (C) {year_now}, \x1b[31mGITSA\x1b[0m", 2)
    t.gen_text("\x1b[94mGitHub Profile ReadMe Terminal, Rev 1011\x1b[0m", 4)
    t.gen_text("Krypton(tm) GIFCPU - 250Hz", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to cancel Memory Test",
        t.num_rows,
    )
    for i in range(0, 65653, 7168):  # 64K Memory
        t.delete_row(7)
        if i < 30000:
            t.gen_text(
                f"Memory Test: {i}", 7, count=2, contin=True
            )  # slow down upto a point
        else:
            t.gen_text(f"Memory Test: {i}", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 64KB OK", 7, count=10, contin=True)
    t.gen_text("", 11, count=10, contin=True)

    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.gen_text("\x1b[96m", 1, count=0, contin=True)  # buffer to be removed
    t.set_font(FONT_FILE_LOGO, 66)
    # t.toggle_show_cursor(True)
    os_logo_text = "GIF OS"
    mid_row = (t.num_rows + 1) // 2
    mid_col = (t.num_cols - len(os_logo_text) + 1) // 2
    effect_lines = gifos.effects.text_scramble_effect_lines(
        os_logo_text, 3, include_special=False
    )
    for i in range(len(effect_lines)):
        t.delete_row(mid_row + 1)
        t.gen_text(effect_lines[i], mid_row + 1, mid_col + 1)

    t.set_font(FONT_FILE_BITMAP, 15)
    t.clear_frame()
    t.clone_frame(5)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mGIF OS v1.0.11 (tty1)\x1b[0m", 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("Obed0101", 3, contin=True)
    t.gen_text("", 4, count=5)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("***********", 4, contin=True)
    t.toggle_show_cursor(False)
    time_now = datetime.now(ZoneInfo("America/Panama")).strftime(
        "%a %b %d %I:%M:%S %p %Z %Y"
    )
    t.gen_text(f"Last login: {time_now} on tty1", 6)

    t.gen_prompt(7, count=5)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)
    t.delete_row(7, prompt_col)  # simulate syntax highlighting
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=3, contin=True)

    #ignore_repos = []
    git_user_details = gifos.utils.fetch_github_stats("Obed0101")
    user_age = gifos.utils.calc_age(20, 12, 2005)
    t.clear_frame()
    top_languages = [lang[0] for lang in git_user_details.languages_sorted]
    user_details_lines = f"""
        \x1b[30;101mObed0101@GitHub\x1b[0m
        --------------
        \x1b[96mOS:     \x1b[93mmacOS / Linux\x1b[0m
        \x1b[96mHost:   \x1b[93mGITSA\x1b[0m
        \x1b[96mKernel: \x1b[93mFull-Stack Dev · MendCode Creator\x1b[0m
        \x1b[96mUptime: \x1b[93m{user_age.years} years, {user_age.months} months, {user_age.days} days\x1b[0m
        \x1b[96mIDE:    \x1b[93mCursor, Neovim, VS Code\x1b[0m
        \x1b[96mShell:  \x1b[93mzsh · MendCode AI terminal\x1b[0m

        \x1b[30;101mContact:\x1b[0m
        --------------
        \x1b[96mEmail:      \x1b[93mobedev.dev@gmail.com\x1b[0m

        \x1b[30;101mGitHub Stats:\x1b[0m
        --------------
        \x1b[96mUser Rating: \x1b[93m{git_user_details.user_rank.level}\x1b[0m
        \x1b[96mTotal Stars Earned: \x1b[93m{git_user_details.total_stargazers}\x1b[0m
        \x1b[96mTotal Commits ({int(year_now) - 1}): \x1b[93m{git_user_details.total_commits_last_year}\x1b[0m
        \x1b[96mTotal PRs: \x1b[93m{git_user_details.total_pull_requests_made}\x1b[0m
        \x1b[96mTotal Contributions: \x1b[93m{git_user_details.total_repo_contributions}\x1b[0m
        \x1b[96mTop Languages: \x1b[93m{', '.join(top_languages[:5])}\x1b[0m
    """
    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(10)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(" -u Obed0101", 1, contin=True)

    t.set_font(FONT_FILE_ASCII, 16, 0)
    t.toggle_show_cursor(False)
    monaLines = r"""
          ,MMM8&&&.
     _...MMMMM88&&&&..._
  .::'''MMMMM88&&&&&&'''::.
 ::     MMMMM88&&&&&&     ::
 '::....MMMMM88&&&&&&....::'
    `''''MMMMM88&&&&''''`
          'MMM8&&&'
    """
    t.gen_text(monaLines, 10)

    t.set_font(FONT_FILE_BITMAP)
    t.toggle_show_cursor(True)
    # t.pasteImage("./temp/Obed0101.jpg", 3, 5, sizeMulti=0.5)
    t.gen_text(user_details_lines, 2, 35, count=5, contin=True)
    t.gen_prompt(t.curr_row)
    t.gen_typing_text(
        "\x1b[92m# the terminal was due for an AI upgrade",
        t.curr_row,
        contin=True,
    )
    # t.save_frame("fetch_details.png")
    t.gen_text("", t.curr_row, count=120, contin=True)

    t.gen_gif()
    # image = gifos.utils.upload_imgbb("output.gif", 129600)  # 1.5 days expiration
    readme_file_content = rf"""<div align="justify">
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="./output.gif">
    <source media="(prefers-color-scheme: light)" srcset="./output.gif">
    <img alt="GIFOS" src="output.gif">
</picture>

<sub><i>Generated automatically by [GIF OS](https://github.com/Obed0101/Obed0101) on {time_now}</i></sub>

<!-- <details>
<summary>More details</summary>

</details> -->
</div>

<!-- Image deletion URL: NONE -->"""
    with open(BASE_DIR / "README.md", "w") as f:
        f.write(readme_file_content)
        print("INFO: README.md file generated")


if __name__ == "__main__":
    main()
