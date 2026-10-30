
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var options = document.querySelector(".wara-language-options");
    var trigger = document.querySelector(".wara-translate-trigger");

    document.querySelectorAll("[data-wara-lang]").forEach(function (link) {
      link.addEventListener("click", function (event) {
        event.preventDefault();

        var language = link.getAttribute("data-wara-lang");

        if (language === "en") {
          window.location.href = window.location.href;
          return;
        }

        var url = "https://translate.google.com/translate?sl=auto&tl=" +
          encodeURIComponent(language) +
          "&u=" + encodeURIComponent(window.location.href);

        window.open(url, "_blank", "noopener,noreferrer");
      });
    });

    if (trigger && options) {
      trigger.addEventListener("click", function () {
        options.hidden = !options.hidden;
        trigger.setAttribute("aria-expanded", String(!options.hidden));
      });
    }
  });
})();
