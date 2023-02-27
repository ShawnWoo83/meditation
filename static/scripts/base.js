/**
 * 初始化table
 * 初始化表达如下：
 * <tr>
 *     <td class='cell_1'></td>
 *     <td class='nn disable' id='#id'></td>
 * </tr>
 */
function createTable() {
    let tbodyData = ''
    for (let i = 1; i < 14; i++) {
        tbodyData += '<tr>';
        tbodyData += "<td class='cell_1'>";
        tbodyData += timeDic[i]
        tbodyData += '</td>';
        for (let j = 1; j < 6; j++) {
            const td_id = j.toString() + i.toString()
            tbodyData += "<td class='nn' id='" + td_id + "'></td>";
        }
        tbodyData += '</tr>';
        if (i == 5) { //在第5行之后追加一个跨列行，用于分隔上下午
            tbodyData += "<tr><td colspan='6' id='test'>&nbsp;</td></tr>"
        }
    }
    $("#tbody1").html(tbodyData);
}


function remove_span(obj) {
    obj.children("span").remove();
}

function add_span(obj, c_id, c_nm) {
    obj.html("<span id='" + c_id + "'>" + c_nm + "</span>")
}

/***
 * 通用的Ajax调取函数；在获取成功应答后，会尝试调用一个与后台控制器方法同名的前端JS方法。
 * @param f_name：需要填写控制器中的方法，同时前端的回调方法需要与该方法同名。
 * @param data
 */
function call_ajax(f_name, data) {
    $.ajax({
        url: '/' + f_name + '/',
        type: 'post',
        data: data,
        success: function (res, textStatus, xhr) {
            if (res["login_required"]) {
                window.location.href = res["redirect_url"]
            } else {
                eval(f_name + "(res)")
            }
        }
    })
}

/***
 * 通过DOM方式创建HTML元素
 * @param e_name
 * @param e_id
 * @param e_class
 * @param e_context
 * @returns {boolean|*}
 */
function create_elem(e_name, e_id, e_class, e_context) {
    if (e_name == undefined || e_name.length == 0) {
        return false;
    }
    let elem = document.createElement(e_name);
    if (e_id != null) elem.id = e_id;
    if (e_class != null) elem.className = e_class;
    if (e_context != null) elem.innerText = e_context;
    return elem;
}


/***
 * 以正则表达式方式，提取URL连接中get段的参数
 * @param p_name
 * @returns {string|null}
 */
function getQueryString(p_name) {
    const reg = new RegExp("(^|&)" + p_name + "=([^&]*)(&|$)", "i");
    let r = location.search.substring(1).match(reg);
    if (r != null) return decodeURI(r[2]);
    return null;
}


/***
 * 获取两个日期间的相差天数
 * 目前是不完善的，需要对日期格式和相关异常进行控制
 * @param begin_date
 * @param end_date
 * @returns {number}
 */
function getDayDiff(begin_date, end_date) {
    const day_diff = (new Date(end_date) - new Date(begin_date)) / (24 * 60 * 60 * 1000);
    return day_diff;
}

/***
 * 以yyyy-mm-dd格式返回当前日期
 * @returns {string}
 */
function get_today_date() {
    const today = new Date();
    let year = today.getFullYear().toString();
    let month = (today.getMonth() + 1).toString().padStart(2, "0");
    let date = today.getDate().toString().padStart(2, "0")
    return year + "-" + month + "-" + date;
}


function parse_res(json_obj) {
    if (json_obj == null) {
        return false;
    }
    const type = json_obj["type"];
    const msg = json_obj["msg"];
    const status = json_obj["status"];
    switch (type) {
        case 'USER_LOGIN':
            $("#msg").html(msg + "<br>");
        case 'USER_REGISTER':
            switch (status) {
                case "00":
                    $("#status").html("注册成功");
                    break;
                default:
                    break;
            }
            $("#msg").html(msg + "<br>");
        case 'AJAX_IS_USER_EXIST':
            switch (status) {
                case "99":
                    $("#msg").html(msg + "<br>");
                default:
                    break;
            }
    }
}