
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".wara-global-tools [data-wara-lang]")
      .forEach(function (link) {
        link.addEventListener("click", function (event) {
          event.preventDefault();

          var language = link.getAttribute("data-wara-lang");

          if (language === "en") {
            window.location.href = window.location.href;
            return;
          }

          var url =
            "https://translate.google.com/translate?sl=en&tl=" +
            encodeURIComponent(language) +
            "&u=" + encodeURIComponent(window.location.href);

          window.open(url, "_blank", "noopener,noreferrer");
        });
      });
  });
})();
