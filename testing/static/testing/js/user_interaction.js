$(document).ready(function() {
    inputs_name_init();
});


function inputs_name_init(){

    let question_inputs = $("input.question_text_input");

    let question_count = 0;

    question_inputs.each(function(i,elem) {
        question_count = question_count + 1;
        let question = $(this);
        let change_answer_type_select = question.parents('.question_text_input_div').siblings('.change_answer_type_select_div').find('.change_answer_type_select');
        question.attr('name', 'question_input_text_' + i);
        change_answer_type_select.attr('name', 'question_answer_type_select_' + i);
        let answer_div = question.parents('.row').siblings('.answers_div');
        let answers_inputs = answer_div.find('.answer_text_input');
        let answer_count = 0;

        answers_inputs.each(function(j,elem) {
            $(this).attr('name', 'question_' + i + '_answer_' + j);
            let is_true_input = $(this).parents('td').siblings('.is_true_td').find('.is_true_input');
            if (change_answer_type_select.children("option:selected").val() == 1) {
                is_true_input.attr('name', 'question_' + i + '_answer_is_true_input');
            }
            else if (change_answer_type_select.children("option:selected").val() == 2) {
                is_true_input.attr('name', 'question_' + i + '_answer_is_true_input_' + j);
            }
        });
    });
    $('#id_question_count').html(`Количество вопросов - ${question_count}`);
}


$("body").on("click", ".delete_answer_button", function(e) {
    $(this).parents('tr').remove();
    inputs_name_init();
});


$("body").on("click", ".delete_question_button", function(e) {
    console.log('delete');
    $(this).parents('div.row').next('br').remove();
    $(this).parents('div.row').remove();
    // $(this).parents('.card').remove();
    inputs_name_init();
});


$("body").on("click", "a.add_answer", function(e) {
    let answer_type_select_id = $(this).parent().parents('.answers_div').siblings('.row').find('.change_answer_type_select').val();
    let table = $(this).parent().siblings('.answer_table');
    let inputs = table.find('.answer_text_input');
    let inputs_count = 0;
    inputs.each(function(i,elem) {
        inputs_count = inputs_count + 1;
    });
    console.log(inputs_count);
    let new_tr = create_new_tr_answer(answer_type_select_id, inputs_count);
    table.find('tbody').append(new_tr);
    inputs_name_init();
});


$("body").on("click", ".change_answer_type_select", function(e) {
    let select_id = $(this).val();
    let answer_div = $(this).parents('.row').siblings('.answers_div');
    let is_true_inputs = answer_div.find('.is_true_input');
    if (select_id === '1') {
        is_true_inputs.each(function(i,elem) {
            $(this).attr('type', 'radio');
            $(this).prop('required', true);
        });
    } else if (select_id === '2') {
        is_true_inputs.each(function(i,elem) {
            $(this).attr('type', 'checkbox');
            $(this).prop('required', false);
        });
    }
    inputs_name_init();
});

$("body").on("focus", "input", function(e) {
    $('div.card').removeClass('card-border-left-on-focus');
    $(this).parents('div.card').addClass('card-border-left-on-focus');
    $('div.div-menu').html('');
    let new_elem = '<div class="d-flex justify-content-center align-items-center flex-column">\n' +
        '<div class="btn btn-light add_question_after" title="Добавить новый вопрос"><i class="far fa-plus-square fa-lg"></i></div><br>\n' +
        '<div class="delete_question_button btn btn-light" title="Удалить вопрос"><i class="far fa-trash-alt fa-lg"></i></div>\n' +
        '</div>'
    $(this).parents('div.col-xl-11').siblings('div.col-xl-1').append(new_elem);
});


$("body").on("click", ".add_question_after", function(e) {

    let new_question = create_new_question();
    let current_question = $(this).parents('div.row');
    $(`${new_question}`).insertAfter(current_question);

});


$("a.add_question").click(function(event) {
    let new_question = create_new_question();
    $('#questions_div').append(new_question);
    inputs_name_init();
    var hiddenElement = document.getElementById("id_bottom");
    // hiddenElement.scrollIntoView({block: "center", behavior: "smooth"});
    $("html, body").animate({ scrollTop: hiddenElement.getBoundingClientRect().top }, "slow");
});


function create_new_tr_answer(answer_type_select_id, inputs_count){
    let input_type; let required_attr; let checked_attr;
    if (answer_type_select_id === '1'){
        input_type = 'radio';
        required_attr = 'required';
        if (inputs_count === 0){
            checked_attr = 'checked';
        } else {
            checked_attr = '';
        }
    }
    else if (answer_type_select_id === '2'){
        input_type = 'checkbox'; required_attr = '';
    }
    let new_td = '<tr><td style="width: 70%;"><input type="text" class="form-control-sm form-control-s answer_text_input" value="Новый ответ"></td>' +
        '<td class="is_true_td"><div class="form-check"> ' +
        '<input class="form-check-input is_true_input" type=' + input_type + ' ' + required_attr + ' ' + checked_attr + '> ' +
        '<label class="form-check-label" for="flexCheckDefault">Является правильным ответом</label><div class="invalid-feedback">Выберите хотя бы один правильный ответ!</div></div></td>' +
        '<td><i class="fas fa-times delete_answer_button"></i></td></tr>';
    return new_td;
}


function create_new_question(){

    let new_answer = '<br><div class="row"><div class="col-xl-11">' +
        '<div class="card shadow bg-white rounded" style="width: 100%;"> ' +
        '<div class="card-body"> ' +
        '<div class="row"> ' +
        '<div class="col-sm-10 question_text_input_div"> ' +
        '<input type="text" class="form-control-s question_text_input" value="Новый вопрос" required> ' +
        '</div> ' +
        '<div class="col-sm-2 change_answer_type_select_div"> ' +
        '<select class="form-select change_answer_type_select"> ' +
        '<option value="1" selected> Один ответ</option> ' +
        '<option value="2"> Несколько ответов</option> ' +
        '</select> ' +
        '</div> ' +
        '</div> ' +
        '<br><br> ' +
        '<div class="answers_div"> ' +
        '<table class="table table-borderless table-hover table-sm answer_table"> ' +
        '<tbody> ' +
        '<tr><td style="width: 70%;"><input type="text" class="form-control-sm form-control-s answer_text_input" value="Новый ответ" required></td>' +
        '<td class="is_true_td"><div class="form-check"> ' +
        '<input class="form-check-input is_true_input" type="radio" checked> ' +
        '<label class="form-check-label" for="flexCheckDefault">Является правильным ответом</label><div class="invalid-feedback">Выберите хотя бы один правильный ответ!</div></div></td>' +
        '<td><i class="fas fa-times delete_answer_button"></i></td></tr>' +
        '</tbody> ' +
        '</table> ' +
        '<br> ' +
        '<small><a class="add_answer btn btn-link btn-sm" style="text-decoration: none;"><i class="fas fa-plus-square"></i> Добавить ответ</a></small> ' +
        '</div></div></div></div>' +
        '<div class="col-xl-1 d-flex align-items-center div-menu"></div>' +
        '</div>'
    return new_answer;
}