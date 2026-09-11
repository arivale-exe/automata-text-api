// Wire the client-side engine to a working demo UI.
document.addEventListener('DOMContentLoaded', function () {
  var input = document.getElementById('tt-input');
  var out = document.getElementById('tt-output');
  if (!input || !out) return;

  function show(data) { out.textContent = JSON.stringify(data, null, 2); }

  var actions = {
    'tt-summarize': function () { show({ summary: TextToolkit.summarize(input.value) }); },
    'tt-keywords': function () { show({ keywords: TextToolkit.keywords(input.value) }); },
    'tt-count': function () { show({ counts: TextToolkit.wordcount(input.value) }); }
  };
  Object.keys(actions).forEach(function (id) {
    var btn = document.getElementById(id);
    if (btn) btn.addEventListener('click', actions[id]);
  });
});
