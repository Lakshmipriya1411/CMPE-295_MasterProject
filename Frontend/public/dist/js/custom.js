$(document).ready(function () {
    $(document).on('focus', ".ingredient-suggest-input", function (event) {
      
        if (event.target.value.length === 0) {
        
            $('.ingredient-suggest-input').parents(':eq(1)').addClass('active');
            $('.fa-plus-circle').addClass('fa-search').removeClass("fa-plus-circle");
            $(".fa-times-circle").show()
            $("#react-autowhatever-1").removeClass("hidden");
        }
    });
    $(document).on('click',".content-wrapper",function(event){
        if($(event.target).is("div")) {
            $('.ingredient-suggest-input').parents(':eq(1)').removeClass('active');
            $('.pantry-ingredient-list-wrapper').css('padding-top','25px');
            $("#react-autowhatever-2").addClass("hidden");
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
           // $('.ingredient-suggest-input').parents(':eq(1)').removeClass('active');
            $('.fa-search').addClass('fa-plus-circle').removeClass("fa-search");
           // $('.pantry-ingredient-list-wrapper').css('padding-top','225px');
            $(".fa-times-circle").hide()
        }
    });
    $(document).on('mouseover', "#react-autowhatever-1", function (event) {
        $(".ingredient-suggest-input").focus()
    });
    $(document).on('click','.fa-times-circle',function(event){
        $(".ingredient-suggest-input").val('');
        $("#react-autowhatever-2").addClass("hidden");
    });
});