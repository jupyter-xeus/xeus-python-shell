from IPython.core.completer import provisionalcompleter, rectify_completions

        scope["shell"] = m_ipython_shell;
        scope["code"] = code;
        scope["cursor_pos"] = cursor_pos;
        exec(py::str(R"(


with provisionalcompleter():
    raw_completions = shell.Completer.completions(code, cursor_pos)
    completions = list(rectify_completions(code, raw_completions))

    comps = []
    for comp in completions:
        comps.append(dict(
            start=comp.start,
            end=comp.end,
            text=comp.text,
            type=comp.type,
        ))

if completions:
    cursor_start = completions[0].start
    cursor_end = completions[0].end
    matches = [c.text for c in completions]
else:
    cursor_start = cursor_pos
    cursor_end = cursor_pos
    matches = []
