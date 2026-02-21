import { useState, useEffect, useCallback } from "react";

export function useTypewriter(
  words: string[],
  typingSpeed = 70,
  deletingSpeed = 40,
  pauseDuration = 2200,
) {
  const [text, setText] = useState("");
  const [wordIndex, setWordIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  const tick = useCallback(() => {
    const currentWord = words[wordIndex];

    if (!isDeleting) {
      setText(currentWord.slice(0, text.length + 1));
      if (text.length + 1 === currentWord.length) {
        setTimeout(() => setIsDeleting(true), pauseDuration);
        return;
      }
    } else {
      setText(currentWord.slice(0, text.length - 1));
      if (text.length === 0) {
        setIsDeleting(false);
        setWordIndex((prev) => (prev + 1) % words.length);
        return;
      }
    }
  }, [text, isDeleting, wordIndex, words, pauseDuration]);

  useEffect(() => {
    const speed = isDeleting ? deletingSpeed : typingSpeed;
    const timeout = setTimeout(tick, speed);
    return () => clearTimeout(timeout);
  }, [tick, isDeleting, typingSpeed, deletingSpeed]);

  return text;
}
