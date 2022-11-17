$(document).ready(function () {
    $(document).on('focus', ".ingredient-suggest-input", function (event) {
        if (event.target.value.length === 0) {
            $('.ingredient-suggest-input').parents(':eq(1)').addClass('active');
            $('.fa-plus-circle').addClass('fa-search').removeClass("fa-plus-circle");
            $(".fa-times-circle").show()
        }
    });
    $(document).on('keyup', ".ingredient-suggest-input", function (event) {
        if (event.target.value.length > 0) {
            $("#react-autowhatever-2").removeClass("hidden");
            $("#react-autowhatever-1").addClass("hidden");
            $('.ingredient-suggest-input').parents(':eq(1)').addClass('active');
            $('.search-plus').removeClass('fa-search').addClass("fa-plus-circle");
            $(".fa-times-circle").show()
        } else {
            $("#react-autowhatever-2").addClass("hidden");
            $("#react-autowhatever-1").removeClass("hidden");
        }
    })
    $(document).on('blur', ".ingredient-suggest-input", function (event) {
        if (event.target.value.length === 0) {
            $('.ingredient-suggest-input').parents(':eq(1)').removeClass('active');
            $('.fa-search').addClass('fa-plus-circle').removeClass("fa-search");
            $(".fa-times-circle").hide()
        }
    });
    $(document).on('mouseover', "#react-autowhatever-1", function (event) {
        $(".ingredient-suggest-input").focus()
    });
});