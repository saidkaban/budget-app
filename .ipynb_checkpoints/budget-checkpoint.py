class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, deposit_amount, deposit_description=""):
        self.ledger.append({
            "amount": deposit_amount,
            "description": deposit_description
        })

    def withdraw(self, withdraw_amount, withdraw_description=""):
        if self.check_funds(withdraw_amount):
            self.ledger.append({
                "amount": -withdraw_amount,
                "description": withdraw_description
            })
            return True
        else:
            return False

    def get_balance(self):
        total_amounts = []
        for i in range(len(self.ledger)):
            total_amounts.append(self.ledger[i]["amount"])
        balance = sum(total_amounts)
        return balance

    def transfer(self, transfer_amount, new_category):
        if self.check_funds(transfer_amount):
            new_category.deposit(transfer_amount,
                                 "Transfer from {}".format(self.category))
            self.withdraw(transfer_amount,
                          "Transfer to {}".format(new_category.category))
            return True
        else:
            return False

    def check_funds(self, check_amount):
        if check_amount <= self.get_balance():
            return True
        else:
            return False

    def __str__(self):
        dash_length = (30 - len(self.category)) // 2
        answer = "*" * dash_length + self.category + "*" * dash_length + "\n"
        for i in range(len(self.ledger)):
            if len(self.ledger[i]["description"]) < 23:
                alignment_length = 28 - len(self.ledger[i]["description"])
            else:
                alignment_length = 5
            answer = answer + self.ledger[i]["description"][:23] + '%.2f'.rjust(
                alignment_length) % self.ledger[i]["amount"] + "\n"
        answer = answer + "Total: {}".format(round((self.get_balance()), 2))

        return answer


def combine_ledgers(category_list):
    all_ledgers = []
    total_spent = 0

    for category in category_list:
        category_ledger = [
            category.ledger[i]["amount"] for i in range(len(category.ledger))
        ]
        category_ledger = list(filter(lambda x: x < 0, category_ledger))
        all_ledgers.append({
            "name": category.category,
            "amount": -sum(category_ledger)
        })
        total_spent = total_spent + -sum(category_ledger)

    for i in range(len(all_ledgers)):
        all_ledgers[i]["amount"] = round(
            all_ledgers[i]["amount"] / total_spent, 2) * 100

    return all_ledgers


def create_spend_chart(categories):
    ledger_list = combine_ledgers(category_list=categories)
    category_names = [i.category for i in categories]
    bar_chart = "Percentage spent by category\n"
    num = 100

    for i in range(11):
        bar_chart = bar_chart + (str(num) + "| ").rjust(5)
        for el in range(len(ledger_list)):
            if ledger_list[el]["amount"] >= num:
                bar_chart = bar_chart + "o" + "  "
            else:
                bar_chart = bar_chart + "   "
        if num == 0:
            bar_chart = bar_chart + "\n" + "    " + "-" * 3 * len(
                category_names) + "-"
        bar_chart = bar_chart + "\n"
        num -= 10

    for i in range(len(max(category_names, key=len))):
        bar_chart = bar_chart + "     "
        for el in range(len(ledger_list)):
            try:
                bar_chart = bar_chart + category_names[el][i] + "  "
            except:
                bar_chart = bar_chart + "   "
        bar_chart = bar_chart + "\n"
    bar_chart = bar_chart.rstrip("\n")
    return bar_chart
