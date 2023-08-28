// Define variables for jQuery, window, and document
var $, window, document;

/* TopButton_function */
$(document).ready(function () {
  "use strict";
  // Initially, hide the element with ID 'topBtn'
  $("#topBtn").css("visibility", "hidden");

  // When the user scrolls the page
  $(window).scroll(function () {
    var scrollval = $(window).scrollTop();

    // If the scroll position is greater than 80 pixels from the top
    if (scrollval > 80) {
      // Make the element with ID 'topBtn' visible
      $("#topBtn").css("visibility", "visible");
    } else {
      // Otherwise, hide the element with ID 'topBtn'
      $("#topBtn").css("visibility", "hidden");
    }
  });

  // When the element with ID 'topBtn' is clicked
  $("#topBtn").click(function () {
    // Scroll smoothly to the top of the page
    $("html ,body").animate(
      {
        scrollTop: 0,
      },
      500
    );
  });
});

/* SearchBarIcon_function */
$(document).ready(function () {
  "use strict";

  // When an element with class 'searchInput' is focused (clicked or selected)
  $(".searchInput").focus(function () {
    // Add a CSS class 'searchBtnActive' to an element with class 'searchBtn'
    $(".searchBtn").addClass("searchBtnActive");
  });

  // When an element with class 'searchInput' loses focus
  $(".searchInput").focusout(function () {
    // Remove the CSS class 'searchBtnActive' from an element with class 'searchBtn'
    $(".searchBtn").removeClass("searchBtnActive");
  });
});
