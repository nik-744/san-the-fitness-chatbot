$(document).ready(function () {
    $("#messageArea").on("submit", function (event) {
        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = hour + ":" + minute;
        var rawText = $("#text").val();

        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

        $("#text").val("");
        $("#messageFormeight").append(userHtml);

        $.ajax({
            contentType: "application/json",  // Set the content type
            data: JSON.stringify({ msg: rawText }),  // Convert data to JSON string
            type: "POST",
            url: "/chat",
        }).done(function (data) {
            var botResponse = data.message;  // Extract the message from the response
            var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + botResponse + '<span class="msg_time">' + str_time + '</span></div></div>';
            $("#messageFormeight").append(botHtml);
        });
        event.preventDefault();
    });
});
// Java script code to make website reload after clicking on logo ( but in this one it is done using html)
// document.addEventListener('DOMContentLoaded',function(){
//     var logo = document.getElementById('logo');
//     if (logo){
//         logo.addEventListener('click',function(){
//             location.reload();
//         });
//     }
// });