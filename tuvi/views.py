from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from .traits_and_rules import physical_traits, personality_traits, rules_1, rules_2, conclusion_levels_1, \
    conclusion_levels_2, advices

def forward_chaining(rules, facts):
    applied_rules = []
    while True:
        new_inferences = False
        for rule_key, rule in rules.items():
            if all(facts.get(cond, False) for cond in rule["conditions"]):
                conclusion_code = rule["conclusion"]
                if conclusion_code not in facts:
                    facts[conclusion_code] = True
                    applied_rules.append(rule_key)
                    new_inferences = True
        if not new_inferences:
            break
    return facts, applied_rules


def home(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'selected_traits[]' in request.POST:
        # Xử lý các đặc điểm tính cách
        personality_input = request.POST.getlist("selected_traits[]")
        facts = {trait: True for trait in personality_input}

        # Áp dụng luật mức 1
        facts, rule_applied_1 = forward_chaining(rules_1, facts)
        level_1_conclusions_keys = [conclusion for conclusion in conclusion_levels_1 if facts.get(conclusion, False)]
        level_1_conclusions = [conclusion_levels_1[key] for key in level_1_conclusions_keys]

        # Lưu các quy tắc mức 1 được áp dụng vào facts để sử dụng cho mức 2
        for rule in rule_applied_1:
            facts[rule] = True

        # Lưu trữ kết quả mức 1 vào session để dùng cho bước tiếp theo
        request.session['level_1_conclusions'] = level_1_conclusions_keys
        request.session['all_facts'] = facts

        return JsonResponse({
            "level_1_conclusions": level_1_conclusions,  # Gửi tên thay vì ký hiệu
            "rule_applied_1": rule_applied_1,
        })

    elif request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'selected_physical_traits[]' in request.POST:
        # Lấy kết luận mức 1 từ session
        level_1_conclusions_keys = request.session.get('level_1_conclusions', [])
        facts = request.session.get('all_facts', {})

        # Thêm các đặc điểm ngoại hình mới vào facts
        selected_physical_traits = request.POST.getlist('selected_physical_traits[]')
        for trait in selected_physical_traits:
            facts[trait] = True

        # Áp dụng luật mức 2
        facts, rule_applied_2 = forward_chaining(rules_2, facts)
        level_2_conclusions_keys = [conclusion for conclusion in conclusion_levels_2 if facts.get(conclusion, False)]
        level_2_conclusions = [conclusion_levels_2[key] for key in level_2_conclusions_keys]

        # Xác định lời khuyên
        advice = [advices.get(key, "Không có lời khuyên.") for key in level_2_conclusions_keys]

        return JsonResponse({
            "level_2_conclusions": level_2_conclusions,  # Gửi tên thay vì ký hiệu
            "rule_applied_2": rule_applied_2,
            "advice": advice,
        })

    return render(request, "home.html", {
        "personality_traits": personality_traits,
        "physical_traits": physical_traits,
    })

