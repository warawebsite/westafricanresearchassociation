(function () {
  "use strict";

  function translateTo(language) {
    if (language === "en") {
      window.location.href = window.location.href;
      return;
    }

    var currentUrl = window.location.href;

    var translateUrl =
      "https://translate.google.com/translate?sl=auto&tl=" +
      encodeURIComponent(language) +
      "&u=" +
      encodeURIComponent(currentUrl);

    window.open(translateUrl, "_blank", "noopener,noreferrer");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll("[data-wara-lang]");

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        translateTo(button.getAttribute("data-wara-lang"));
      });
    });

    var trigger = document.querySelector(".wara-translate-trigger");
    var options = document.querySelector(".wara-language-options");

    if (trigger && options) {
      trigger.addEventListener("click", function () {
        var hidden = options.hidden;
        options.hidden = !hidden;
        trigger.setAttribute("aria-expanded", String(hidden));
      });

      trigger.setAttribute("aria-expanded", "true");
    }
  });
})();
