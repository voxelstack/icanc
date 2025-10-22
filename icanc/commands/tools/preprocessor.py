import click
from ..common.exception import InvalidSourceException, UnknownIncludeException, UnknownPragmaException
from ..common.paths import icanc_path
from ..common.rc import config
import os
import re

def preprocess(judge, problem, solution, path, cache, uglify):
    author = config.get("author")
    email = config.get("email")
    repository = config.get("repository")

    credits = ""
    if author:
        credits += f" Solution by {author}"
        if email:
            credits += f" <{email}>"
        credits += "\n"
    if repository:
        credits += f" * {repository}\n"
    if author or email or repository:
        credits += " *"

    header = f"""/*
 * {judge}/{problem} {solution}.c
 *{credits}
 * Powered by icanc
 * https://github.com/voxelstack/icanc
 */
"""
    
    return "{}\n{}".format(header, "".join(preprocess_source(path, cache, [], uglify)["source"]))

def preprocess_source(path, cache, included, uglify):
    if path in cache.values():
        return cache[path]
    
    # TODO Relative paths would be clearer for errors.
    filename = f"{os.path.basename(path)}"
    with open(path, "r", encoding="utf-8") as f:
        source = iter(f.readlines())
        preprocessed_source = []
        pragma_once = False
        last_line_empty = False

        lineno = 0
        line = next(source, None)
        while line is not None:
            trimmed = line.lstrip()

            if uglify:
                line = re.sub(r"\s*//.*$", "", line)
                if trimmed.startswith("/*"):
                    while line is not None and "*/" not in line:
                        line = next(source, None)
                        trimmed = line.lstrip()
                        lineno += 1
                    line = re.sub(r"^.*\*/", "", line)
                    continue
                elif re.match(r"^\s*\n", line):
                    line = next(source, None)
                    trimmed = line.lstrip()
                    lineno += 1
                    continue

            # Yeah yeah.
            # String matching is enough here but I do speak AST.
            #
            # https://github.com/voxelstack/atlas/blob/main/src/atlas/comms_derive/src/shareable.rs
            # https://xkcd.com/1171/
            if trimmed.startswith("#pragma"):
                pragma = trimmed[len("#pragma"):].lstrip()
                if pragma.startswith("once"):
                    pragma_once = True
                elif pragma.startswith("icanc"):
                    pragma_icanc = pragma[len("icanc"):].lstrip()
                    if pragma_icanc.startswith("include"):
                            while True:
                                line = next(source, None).lstrip()
                                lineno += 1
                                if line is None or not line.startswith("#include"):
                                    if line.startswith("#pragma icanc end"):
                                        break
                                    raise InvalidSourceException("include directive", f"{filename}:{lineno}", f"Expected #include or #pragma icanc end, got \"{line.strip()}\".")

                                include_file = line[len("#include"):].strip()[1:-1]
                                include_path = icanc_path("include", include_file)
                                if not os.path.exists(include_path):
                                    raise UnknownIncludeException(include_file, f"{filename}:{lineno}")
                                include = preprocess_source(include_path, cache, included, uglify)
                                if not include["once"] or include_path not in included:
                                    if not uglify:
                                        preprocessed_source.append("// BEGIN {}\n".format(include_file))
                                        preprocessed_source.extend(include["source"])
                                        preprocessed_source.append("// END {}\n".format(include_file))
                                    else:
                                        preprocessed_source.extend(include["source"])
                                    
                                    included.append(include_path)
                    else:
                        raise UnknownPragmaException(f"\"{pragma_icanc.strip()}\"", f"{filename}:{lineno}")
                line = next(source, None)
                lineno += 1
                continue

            current_line_empty = len(trimmed) == 0
            # Since we are omitting some lines when generating the submission,
            # it's common to have double line breaks which look bad.
            # Skip them.
            if not (last_line_empty and current_line_empty):
                preprocessed_source.append(line)
            last_line_empty = current_line_empty

            line = next(source, None)
            lineno += 1

    source = {
        "source": preprocessed_source,
        "once": pragma_once,
    }
    cache[path] = source
    return source
