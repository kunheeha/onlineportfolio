$(document).ready(function () {

	// Scrolling
	$('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 72,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Isotope
    var container = $('.portfolioContainer');
    container.isotope({
        filter : '*'
    });

    $('.portfolio-nav li[data-filter = "*"]').addClass('active')

    $('.portfolio-nav li').click(function() {
        $('.portfolio-nav .active').removeClass('active');
        $(this).addClass('active');

        var selector = $(this).attr('data-filter');
        container.isotope({
            filter : selector
        });
    });

    // Fancybox
    $("[data-fancybox]").fancybox({});

	// Navbar collapse after clicking nav link
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });



    // Add active class to navlink on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 74,
    });

    // Collapse navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 180) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };

    navbarCollapse();
    // Collapse navbar on scroll
    $(window).scroll(navbarCollapse);


    // WOW
    var wow = new WOW(
      {
        boxClass:     'wow',      // animated element css class (default is wow)
        animateClass: 'animated', // animation css class (default is animated)
        offset:       0,          // distance to the element when triggering the animation (default is 0)
        mobile:       true,       // trigger animations on mobile devices (default is true)
        live:         true,       // act on asynchronously loaded content (default is true)
        callback:     function(box) {
          // the callback is fired every time an animation is started
          // the argument that is passed in is the DOM node being animated
        },
        scrollContainer: null // optional scroll container selector, otherwise use window
      }
    );
    wow.init();

    // Education and Strenghts section
    var educationSection = $('.education-section');
    var educationbtn = $('#educationbtn');
    $('.education-section .active').removeClass('active');

    educationbtn.on('click', function() {
        if (educationSection.hasClass('active')) {
            educationSection.removeClass('active');
        } else if (!educationSection.hasClass('active')) {
            educationSection.addClass('active');
        }
    });

    // copy email to clipboard
    $('.emailLink').on('click', function () {
        const myEmail = 'kunheeha@gmail.com';
        navigator.clipboard.writeText(myEmail).then(
            function(){alert('Email copied to clipboard')});
    });

    // Contact form
    var contactform = $('.contact-form');
    var displayMsg = $('.formMessages');
    contactform.submit(function(event) {
        event.preventDefault();
        displayMsg.addClass('alert');
        displayMsg.addClass('alert-info');
        displayMsg.text('Please wait');
        var formData = contactform.serialize();
        $.ajax({
            type: 'POST',
            url: '/contact',
            data: formData,
            success: function(response) {
                console.log(response);
                if (response.status) {
                    displayMsg.removeClass('alert-info');
                    displayMsg.addClass('alert-success');
                    displayMsg.text('Your message has been sent. Please check your email');
                    $('#inputFname').val('');
                    $('#inputLname').val('');
                    $('#inputEmail').val('');
                    $('#inputMessage').val('');
                } else if (!response.status) {
                    displayMsg.removeClass('alert-info');
                    displayMsg.addClass('alert-danger');
                    displayMsg.text('Message failed to send. Please check you have filled in the form correctly');
                }
            }
        });
    });



});
