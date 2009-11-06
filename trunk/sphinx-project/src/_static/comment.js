DESELEMENT = "h1,ul,div.section h2,div.section p";
COMMENTURL = "/pymotwcn/comment/";

function get_dt(){
    var dt = {};
    dt["title"] = $("a.documents:first").html();
    dt["page"] = $("div.bodywrapper div.body div.section:first").attr("id");
    dt["version"] = DOCUMENTATION_OPTIONS.VERSION;
    return dt;
}

function loading(msg){
    if (!$("div#loading").length) {
        $("body").prepend('<div id="loading"></div>');
    }
    $("div#loading").css("left", $(window).width()/2-30).html(msg+'ing...');
}

function unloading(){
    $("body div#loading").remove();
}

function load_comment(){
    var dt = get_dt();
    dt["action"] = "load";
    $.ajax({
        url: COMMENTURL,
        data: dt,
        type:"POST",
        beforeSend: function(){
            loading("load");
        },
        complete: function(req, status){
            unloading();
            if ("success" == status){
                var result = eval('('+req.responseText+')');
                $("div.body > div.section").find(DESELEMENT).each(function(){
                    var mykey = hex_md5($(this).html());
                    try {
                        if (result[mykey]) {
                            var i, cmt, box = get_commentbox($(this));
                            for (i in result[mykey]) {
                                cmt = result[mykey][i];
                                add_a_comment(box, cmt[0], cmt[1], cmt[2]);
                            }
                            $(this).prev("div.comment").find("a.comment_link").attr("title", (++i)+" comments");
                        }
                    } catch(e) {alert(e);}
                });
            }
        }
    });
}
function show_error(obj, msg){
    var outer = obj.prev();
    if (!outer.children("span.error").length) {
        outer.append('<span class="error"></span>');
    }
    outer.children("span.error").html(msg);
}
function hide_error(obj){
    obj.prev().children("span.error").remove();
}
function click_send(){
    var submit = $(this);
    var box = submit.parents("div.commentbox");
    var text = box.find("textarea.comment_text");
    var sender = box.find("input.comment_name");
    var validate = true;
    if (text.val().length<1) {
        show_error(text, "评论内容为空!");
        validate = false;
    } else hide_error(text);
    if (sender.val().length<1)  {
        show_error(sender, "提交者为空!");
        validate = false;
    } else hide_error(sender);
    // todo: other check
    if (!validate) return;
    var dt = get_dt();
    dt["action"] = "send";
    dt["para"] = hex_md5(box.prev(DESELEMENT).html());
    dt["sender"] = sender.val();
    dt["text"] = text.val();
    $.ajax({
        url: COMMENTURL,
        data: dt,
        type:"POST",
        beforeSend: function(){
            loading("send");
            submit.hide();
            submit.after('<img src="../_static/throbber.gif" alt="waiting" />');
        },
        complete: function(req, status){
            unloading();
            if ("success" == status){
                var result = eval('('+req.responseText+')');
                if (result.error) {
                    show_error(text, result.error);
                } else if (result.sender) {
                    add_a_comment(box, result.sender, result.date, result.text);
                }
            }
            submit.next("img").remove();
            submit.show();
            sender.val('');
            text.val('');
        }
    });
}
function add_a_comment(box, sender, date, text){
                    var dl = box.find("dl");
                    if (!dl.length) {
                        box.prepend("<p>现有评论: </p><dl></dl><hr />");
                        dl = box.find("dl");
                    }
                    dl.prepend("<dt><b>"+sender+"</b> "+date+"</dt><dd>"+text+"</dd>");
}
function get_commentbox(outer){
    if(!outer.next("div.commentbox").length){
        outer.after('<div class="commentbox" style="display:none;"><p>评论内容:</p><textarea class="comment_text" rows="4" style="width:100%"></textarea><p>评论者(名字或者邮箱):</p><input class="comment_name" type="text" maxlength="30" /><input class="comment_send" type="button" value="发送"/></div>');
        outer.next("div.commentbox").find("input.comment_send").bind("click", click_send);
    }
    return outer.next("div.commentbox");
}
function show_commentbox(obj){
    var outer = obj.parent("div.comment").next();
    get_commentbox(outer).slideDown();
    obj.children("div").css("background-position", "0 0");
    outer.css("background-color", "#FFFDC9");
}
function hide_commentbox(obj){
    obj.parent("div.comment").next().css("background-color", "white").next("div.commentbox").slideUp();
    obj.children("div").css("background-position", "-16px 0");
}
function clean_tag(st){
    return st.replace(/<[^>]+>?[^<]*>/g, '');
}
$(document).ready(function(){
    $("div.body > div.section").find(DESELEMENT).each(function(){
        if (!$(this).prev("div.comment").length) {
            $(this).before('<div class="comment"><a class="comment_link" title="leave your comments"><div></div></a><a class="email_link" title="groups"><div></div></a></div>');
        }
    });
    $("div.comment").css("left", $("div.document").offset().left+2);
    load_comment();
    $("a.comment_link").toggle(function(){
        show_commentbox($(this));
    }, function(){
        hide_commentbox($(this));
    });
    $("a.email_link").hover(function(){
        if ($(this).attr("href") == null) {
            var sub = $("div.bodywrapper div.body div.section:first h1").html();
            var body = $(this).parent("div.comment").next().html();
            sub = clean_tag(sub);
            body = clean_tag(body);
            if (body.length>100) {
                body = body.substring(0, 100)+"...";
            }
            $(this).attr("href", "http://groups.google.com/group/pymotwcn/post?hl=zh-CN&subject="+sub+"&body="+body);
            $(this).attr("target", "_blank");
        }
    }, function(){
    });
});

