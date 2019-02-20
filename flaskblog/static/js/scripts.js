var $, window, document;

/* TopButton_function */
$(document).ready(function () {
    'use strict';
    $('#topBtn').css('visibility', 'hidden');
    $(window).scroll(function () {
        var scrollval = $(window).scrollTop();
        if (scrollval > 80) {
            $('#topBtn').css('visibility', 'visible');
        } else {
            $('#topBtn').css('visibility', 'hidden');
        }
    });
    $("#topBtn").click(function () {
        $('html ,body').animate({
            scrollTop: 0
        }, 500);
    });
});

/* MenuIcon_function */
$(document).ready(function () {
    'use strict';
    $(".btnH").on("click", function () {
        $('.menu').toggleClass("show");
        if($(this).find('i').hasClass('fa-bars')) {
            $(this).find('i').removeClass('fa-bars');
            $(this).find('i').addClass('fa-times');
        } else {
            $(this).find('i').removeClass('fa-times');
            $(this).find('i').addClass('fa-bars');
        };
    });
});



/* AccountMenu_function */
$(document).ready(function () {
    'use strict';
    $('#loginBtn').on('click', function () {
        $('.userAccountMenu').toggleClass('userAccountMenuShow');
    });
});
/* AccountMenu_mobile_function */
$(document).ready(function () {
    'use strict';
    $('#loginBtnSmall').on('click', function () {
        $('.userAccountMenu').toggleClass('userAccountMenuShow');
        if($(this).find('i').hasClass('fa-user')) {
            $(this).find('i').removeClass('fa-user');
            $(this).find('i').addClass('fa-times');
        } else {
            $(this).find('i').removeClass('fa-times');
            $(this).find('i').addClass('fa-user');
        };
    });
});

/* AdminMenu_function */
$(document).ready(function() {
    $('.btnAdminMenu').on('click', function () {
        $('.sideMenu').toggleClass('sideMenuShow');
        if($(this).find('i').hasClass('fa-bars')) {
            $(this).find('i').removeClass('fa-bars');
            $(this).find('i').addClass('fa-times');
        } else {
            $(this).find('i').removeClass('fa-times');
            $(this).find('i').addClass('fa-bars');
        };     
    });
})

/* SearchBarIcon_function */
$(document).ready(function() {
    'use strict';
    $('.searchInput').focus(function () {
        $('.searchBtn').addClass('searchBtnActive');
    });
    $('.searchInput').focusout(function () {
        $('.searchBtn').removeClass('searchBtnActive');
    });
})

/* Removing Alert Div */
$(document).ready(function() {
    $(this).find('.alert').delay(3000).fadeOut('slow');
})

