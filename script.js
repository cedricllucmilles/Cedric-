(() => {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const progressLabel = document.getElementById("progressLabel");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const dotsRoot = document.getElementById("dots");
  const deck = document.getElementById("deck");
  let index = 0;

  function renderDots() {
    dotsRoot.innerHTML = "";
    slides.forEach((slide, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "dot" + (i === index ? " is-active" : "");
      btn.setAttribute("aria-label", `Ir a diapositiva ${i + 1}: ${slide.dataset.title || ""}`);
      btn.addEventListener("click", () => goTo(i));
      dotsRoot.appendChild(btn);
    });
  }

  function goTo(next) {
    index = Math.max(0, Math.min(slides.length - 1, next));
    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === index);
    });
    progressLabel.textContent = `${index + 1} / ${slides.length}`;
    prevBtn.disabled = index === 0;
    nextBtn.disabled = index === slides.length - 1;
    renderDots();
  }

  function next() {
    goTo(index + 1);
  }

  function prev() {
    goTo(index - 1);
  }

  prevBtn.addEventListener("click", prev);
  nextBtn.addEventListener("click", next);

  document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight" || event.key === " " || event.key === "PageDown") {
      event.preventDefault();
      next();
    } else if (event.key === "ArrowLeft" || event.key === "PageUp") {
      event.preventDefault();
      prev();
    } else if (event.key === "Home") {
      event.preventDefault();
      goTo(0);
    } else if (event.key === "End") {
      event.preventDefault();
      goTo(slides.length - 1);
    } else if (event.key === "f" || event.key === "F") {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen?.();
      } else {
        document.exitFullscreen?.();
      }
    }
  });

  let touchStartX = 0;
  deck.addEventListener(
    "touchstart",
    (event) => {
      touchStartX = event.changedTouches[0].screenX;
    },
    { passive: true }
  );

  deck.addEventListener(
    "touchend",
    (event) => {
      const delta = event.changedTouches[0].screenX - touchStartX;
      if (Math.abs(delta) < 50) return;
      if (delta < 0) next();
      else prev();
    },
    { passive: true }
  );

  goTo(0);
  deck.focus();
})();
