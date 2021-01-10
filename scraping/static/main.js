function login(){
    var username = $("#username").val();
    var password = $("#password").val();
    console.log(username)
    console.log(password)
    if(username!="" && password!=""){
        $.ajax({
            url: "http://127.0.0.1:8000/get_token/",
            type: "POST",
            data:{
                'username': username,
                'password': password,
            },
            success:function(data){
                document.cookie="token="+data['token'];
                console.log(data)
                window.location.href = "/scrape/";
            },
            error:function(data){
                console.log(data)
            }
        });
    }
};

function verify(){
    tokens = (document.cookie).toString().split(";");
    var token;
    tokens.forEach(ele => {
        if (ele.includes("token")){
            token = ele.split('=')[1]
        } 
    })
    $.ajax({
        url : "http://127.0.0.1:8000/verify_token/", 
        type : "GET",
        headers : {
            "Authentication": "JWT " + token
        },
        success:function(data){
            console.log("Success")
            console.log(data['status'])
            if (data['status'] == false){
                window.location.href = "http://127.0.0.1:8000/";
            }
        },
        error:function(data){
            window.location.href = "http://127.0.0.1:8000/";
            console.log(data)
        }
    });
};

function check_url(){
    var link = $('#url').val()
    $.ajax({
        url: "/check_url/",
        type: "POST",
        data: JSON.stringify({
            'url' : link 
        }),
        success:function(data){
            console.log(data)
            if (data['status'] == true){
                console.log("success")
                window.location.href = "http://127.0.0.1:8000/completed/"
            }
            else {
                alert("Invalid URL.")
            }
        },
        error:function(data){
            console.log(data)
            console.log("vayena")
        },
    });
};
