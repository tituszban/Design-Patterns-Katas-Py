from .strategy import create_monthly_repayment, LoanInfo, MonthlyRepayment


def test_equal_amounts():
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
    assert create_monthly_repayment(example) == MonthlyRepayment(
        loan_id="123-456",
        payment=319.4444,
        amount_remaining=9722.2222,
        remaining_duration=35,
    )

# TODO: Add more tests