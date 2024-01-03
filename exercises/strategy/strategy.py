from dataclasses import dataclass


# Models:
# You may not modify these models, as theoretical systems outside this exercise expect to use these models to communicate with your method
@dataclass
class LoanInfo:
    loan_id: str
    loan_kind: str
    original_duration: int
    remaining_duration: int
    interest: float
    amount: float
    current_credit_score: int
    libor: float


@dataclass
class MonthlyRepayment:
    loan_id: str
    payment: float
    amount_remaining: float
    remaining_duration: int


def create_monthly_repayment(loan_info: LoanInfo) -> MonthlyRepayment:
    interest_payment = loan_info.amount * loan_info.interest / 12 / 100
    variable_interest_payment = loan_info.amount * (loan_info.interest + loan_info.libor) / 12 / 100
    repayment = loan_info.amount / loan_info.remaining_duration
    duration_so_far = loan_info.original_duration - loan_info.remaining_duration
    if loan_info.loan_kind == "interest_only":
        if loan_info.remaining_duration <= 1:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(interest_payment + loan_info.amount, 4),
                amount_remaining=round(0, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(interest_payment, 4),
            amount_remaining=round(loan_info.amount, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "interest_only_variable":
        if loan_info.remaining_duration <= 1:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(variable_interest_payment + loan_info.amount, 4),
                amount_remaining=round(0, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(variable_interest_payment, 4),
            amount_remaining=round(loan_info.amount, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "interest_and_repayment":
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount - repayment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "v_interest_and_repayment":
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(variable_interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount - repayment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "introductory_offer_3":
        if duration_so_far < 3:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(0, 4),
                amount_remaining=round(loan_info.amount + interest_payment, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount - repayment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "introductory_offer_12":
        if duration_so_far < 12:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(0, 4),
                amount_remaining=round(loan_info.amount + variable_interest_payment, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(variable_interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount - repayment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "introductory_offer_interst_only_6":
        if duration_so_far < 6:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(interest_payment, 4),
                amount_remaining=round(loan_info.amount, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount - repayment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "introductory_offer_interst_only_9":
        if duration_so_far < 9:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(interest_payment, 4),
                amount_remaining=round(loan_info.amount, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount - repayment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "good_credit_score":
        if loan_info.current_credit_score >= 700:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(repayment, 4),
                amount_remaining=round(loan_info.amount - repayment, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount - repayment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "very_good_credit_score":
        if loan_info.current_credit_score >= 850:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(repayment, 4),
                amount_remaining=round(loan_info.amount - repayment, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(variable_interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount - repayment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "bad_credit_score":
        if loan_info.current_credit_score < 650:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(interest_payment * 2 + repayment, 4),
                amount_remaining=round(loan_info.amount - repayment, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount + interest_payment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )
    if loan_info.loan_kind == "very_bad_credit_score":
        if loan_info.current_credit_score < 500:
            return MonthlyRepayment(
                loan_id=loan_info.loan_id,
                payment=round(interest_payment * 2 + repayment, 4),
                amount_remaining=round(loan_info.amount - repayment, 4),
                remaining_duration=loan_info.remaining_duration - 1,
            )
        return MonthlyRepayment(
            loan_id=loan_info.loan_id,
            payment=round(interest_payment + repayment, 4),
            amount_remaining=round(loan_info.amount + interest_payment, 4),
            remaining_duration=loan_info.remaining_duration - 1,
        )

    return MonthlyRepayment(
        loan_id=loan_info.loan_id,
        payment=round(interest_payment + repayment, 4),
        amount_remaining=round(loan_info.amount - repayment, 4),
        remaining_duration=loan_info.remaining_duration - 1,
    )


def run_example():
    example = LoanInfo(
        loan_id="123-456",
        loan_kind="interest_and_repayment",
        original_duration=36,
        remaining_duration=36,
        interest=5,
        amount=10000,
        current_credit_score=700,
        libor=3,
    )

    print(f"Example: {example}")
    repayment_info = create_monthly_repayment(example)
    print(f"Loan Id: {repayment_info.loan_id}")
    print(f"Payment: {repayment_info.payment}")
    print(f"Amount remaining: {repayment_info.amount_remaining}")
    print(f"Amount duration: {repayment_info.remaining_duration}")


if __name__ == "__main__":
    run_example()
