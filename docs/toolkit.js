/**
 * Text Toolkit — client-side engine.
 * Runs the same algorithms as server.py entirely in the browser.
 * Zero hosting cost. Publicly reachable. Real work.
 */

(function (global) {
  'use strict';

  function summarize(text, maxSentences) {
    if (maxSentences == null) maxSentences = 3;
    var sentences = text
      .replace(/\s+/g, ' ')
      .split(/(?<=[.!?])\s+/)
      .map(function (s) { return s.trim(); })
      .filter(function (s) { return s.length > 0; });
    if (sentences.length <= maxSentences) return sentences.join(' ');
    // Score by word frequency, keep top-N in original order.
    var freq = {};
    sentences.forEach(function (s) {
      s.toLowerCase().split(/\W+/).forEach(function (w) {
        if (w.length > 3) freq[w] = (freq[w] || 0) + 1;
      });
    });
    var scored = sentences.map(function (s, i) {
      var score = 0;
      s.toLowerCase().split(/\W+/).forEach(function (w) {
        if (freq[w]) score += freq[w];
      });
      return { i: i, s: s, score: score / Math.max(1, s.split(' ').length) };
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    var top = scored.slice(0, maxSentences).sort(function (a, b) { return a.i - b.i; });
    return top.map(function (x) { return x.s; }).join(' ');
  }

  function keywords(text, n) {
    if (n == null) n = 5;
    var stop = {
      this: 1, that: 1, with: 1, from: 1, they: 1, have: 1, will: 1, your: 1,
      what: 1, when: 1, which: 1, their: 1, there: 1, about: 1, would: 1,
      these: 1, those: 1, been: 1, were: 1, into: 1, more: 1, than: 1, then: 1
    };
    var words = text.toLowerCase().match(/\b[a-z]{4,}\b/g) || [];
    var freq = {};
    words.forEach(function (w) {
      if (!stop[w]) freq[w] = (freq[w] || 0) + 1;
    });
    return Object.keys(freq)
      .map(function (w) { return { w: w, c: freq[w] }; })
      .sort(function (a, b) { return b.c - a.c || (a.w < b.w ? -1 : 1); })
      .slice(0, n)
      .map(function (x) { return x.w; });
  }

  function wordcount(text) {
    var words = text.trim() ? text.trim().split(/\s+/).length : 0;
    var sentences = (text.match(/[.!?]+/g) || []).length;
    return {
      words: words,
      characters: text.length,
      charactersNoSpaces: text.replace(/\s/g, '').length,
      sentences: sentences,
      paragraphs: text.trim() ? text.trim().split(/\n\s*\n/).length : 0,
      readingSeconds: Math.round((words / 200) * 60)
    };
  }

  global.TextToolkit = { summarize: summarize, keywords: keywords, wordcount: wordcount };
  if (typeof module !== 'undefined' && module.exports) module.exports = global.TextToolkit;
})(typeof window !== 'undefined' ? window : this);
