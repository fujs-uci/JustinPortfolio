let lastScrollTop = 0,
    delta = 50,
    timeout,
    busy = false;

let calls = 0;

// If Hash exists in url, go to it
$(document).ready(function () {
    // make section-active to the section in url on page load
    if (window.location.hash) {
        let section = $(window.location.hash.toString());
        let currentSection = $('div.section-active');
        currentSection.removeClass('section-active');
        $(section).addClass('section-active');
        lastScrollTop = $(section).offset().top;

        $('html, body').animate({
            scrollTop: lastScrollTop
        });
    }
});

// Modal menu link control and close
$(document).on("click", ".menu-modal-link", function () {
    // close the modal menu and assign section-action
    let section = $(this).find('a').attr('href');
    if (section.toString()[0] === '#') {
        let currentSection = $('div.section-active');
        currentSection.removeClass('section-active');
        $(section).addClass('section-active');
        lastScrollTop = $(section).offset().top;
    }
    $('#nav-modal').modal('hide');
});

