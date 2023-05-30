
$(document).ready(function() {

    $("#settingSaveBtn").on("click", function(){
        let getUserCountry = document.getElementById("newsCountry").value;
        let getUserLanguage = document.getElementById("newsLanguage").value;

        $.ajax({
            type: "get",
            url: "/set",
            data: {
                country: getUserCountry,
                language: getUserLanguage
            },
            success: function (response) {
                location.href = "/";
            }
        });
    });
});