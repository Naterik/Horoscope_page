from django.http import JsonResponse
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
    # Xử lý POST request đầu tiên cho các đặc điểm tính cách
    if request.method == "POST" and request.headers.get(
            'x-requested-with') == 'XMLHttpRequest' and 'selected_traits[]' in request.POST:
        personality_input = request.POST.getlist("selected_traits[]")
        facts = {trait: True for trait in personality_input}

        # Áp dụng luật mức 1
        facts, rule_applied_1 = forward_chaining(rules_1, facts)
        level_1_conclusions = [conclusion for conclusion in conclusion_levels_1 if facts.get(conclusion, False)]

        # Lưu trữ kết quả vào session để sử dụng cho bước tiếp theo
        request.session['level_1_conclusions'] = level_1_conclusions

        return JsonResponse({
            "level_1_conclusions": level_1_conclusions,
            "rule_applied_1": rule_applied_1,
        })

    # Xử lý POST request cho các đặc điểm ngoại hình
    elif request.method == "POST" and request.headers.get(
            'x-requested-with') == 'XMLHttpRequest' and 'selected_physical_traits[]' in request.POST:
        # Lấy kết luận mức 1 từ session
        level_1_conclusions = request.session.get('level_1_conclusions', [])
        facts = {conclusion: True for conclusion in level_1_conclusions}

        selected_physical_traits = request.POST.getlist('selected_physical_traits[]')
        for trait in selected_physical_traits:
            facts[trait] = True

        # Áp dụng luật mức 2
        facts, rule_applied_2 = forward_chaining(rules_2, facts)
        level_2_conclusions = [conclusion for conclusion in conclusion_levels_2 if facts.get(conclusion, False)]

        if level_2_conclusions:
            destiny = level_2_conclusions[0]
            advice = advices.get(destiny, "Không có lời khuyên.")
        else:
            destiny = "Không có kết luận."
            advice = "Không có lời khuyên."

        return JsonResponse({
            "destiny": destiny,
            "rule_applied_2": rule_applied_2,
            "advice": advice,
        })

    # Trường hợp GET request hoặc lần đầu load trang
    return render(request, "home.html", {
        "personality_traits": personality_traits,
        "physical_traits": physical_traits,
    })
