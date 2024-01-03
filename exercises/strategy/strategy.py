from dataclasses import dataclass
from abc import ABC, abstractmethod


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


@dataclass
class Repayment:
    payment: float
    amount_remaining_change: float


class InterestStrategyABC(ABC):
    @abstractmethod
    def calculate_interest(self, loan_info: LoanInfo) -> float:
        raise NotImplementedError


class FixedInterestStrategy(InterestStrategyABC):
    def calculate_interest(self, loan_info: LoanInfo) -> float:
        return loan_info.interest / 12 * loan_info.amount


class VariableInterestStrategy(InterestStrategyABC):
    def __init__(self, libor: float):
        self._libor = libor

    def calculate_interest(self, loan_info: LoanInfo) -> float:
        return (loan_info.interest + self._libor) / 12 * loan_info.amount


class RepaymentStrategyABC(ABC):
    def __init__(self, interest_strategy: InterestStrategyABC):
        self._interest_strategy = interest_strategy

    def _calculate_interest_payment(self, loan_info: LoanInfo):
        return self._interest_strategy.calculate_interest(loan_info)

    def _repayment_payment(self, loan_info: LoanInfo):
        return loan_info.amount / loan_info.remaining_duration

    @abstractmethod
    def calculate_monthly_repayment(self, loan_info: LoanInfo) -> Repayment:
        raise NotImplementedError


class InterestOnlyRepaymentStrategy(RepaymentStrategyABC):
    def calculate_monthly_repayment(self, loan_info: LoanInfo) -> Repayment:
        interest_payment = self._calculate_interest_payment(loan_info)
        if loan_info.remaining_duration <= 1:
            return Repayment(loan_info.amount + interest_payment, -loan_info.amount)
        return Repayment(interest_payment, 0)


class InterestAndRepaymentStrategy(RepaymentStrategyABC):
    def calculate_monthly_repayment(self, loan_info: LoanInfo) -> Repayment:
        repayment = self._repayment_payment(loan_info)
        interest = self._calculate_interest_payment(loan_info)
        return Repayment(repayment + interest, -repayment)


class IntroductoryOfferRepaymentStrategy(InterestAndRepaymentStrategy):
    def __init__(self, interest_strategy: InterestStrategyABC, offer_duration):
        super().__init__(interest_strategy)
        self._offer_duration = offer_duration

    def calculate_monthly_repayment(self, loan_info: LoanInfo) -> Repayment:
        duration_so_far = loan_info.original_duration - loan_info.remaining_duration
        if duration_so_far < self._offer_duration:
            return Repayment(0, self._calculate_interest_payment(loan_info))

        return super().calculate_monthly_repayment(loan_info)


class IntroductoryInterestOnlyOfferRepaymentStrategy(IntroductoryOfferRepaymentStrategy):
    def calculate_monthly_repayment(self, loan_info: LoanInfo) -> Repayment:
        duration_so_far = loan_info.original_duration - loan_info.remaining_duration
        if duration_so_far < self._offer_duration:
            return Repayment(self._calculate_interest_payment(loan_info), 0)

        return super().calculate_monthly_repayment(loan_info)


class GoodCreditScoreRepaymentStrategy(InterestAndRepaymentStrategy):
    def __init__(self, interest_strategy: InterestStrategyABC, threshold: int):
        super().__init__(interest_strategy)
        self._threshold = threshold

    def calculate_monthly_repayment(self, loan_info: LoanInfo) -> Repayment:
        repayment = self._repayment_payment(loan_info)
        if loan_info.current_credit_score >= self._threshold:
            return Repayment(repayment, -repayment)
        return super().calculate_monthly_repayment(loan_info)


class BadCreditScoreRepaymentStrategy(InterestAndRepaymentStrategy):
    def __init__(self, interest_strategy: InterestStrategyABC, threshold: int):
        super().__init__(interest_strategy)
        self._threshold = threshold

    def calculate_monthly_repayment(self, loan_info: LoanInfo) -> Repayment:
        repayment = self._repayment_payment(loan_info)
        interest = self._calculate_interest_payment(loan_info)
        if loan_info.current_credit_score < self._threshold:
            return Repayment(repayment + interest * 2, -repayment)
        return super().calculate_monthly_repayment(loan_info)


def calculate_repayment(loan_info: LoanInfo, strategy: RepaymentStrategyABC) -> MonthlyRepayment:
    repayment = strategy.calculate_monthly_repayment(loan_info)
    return MonthlyRepayment(
        loan_id=loan_info.loan_id,
        payment=round(repayment.payment, 4),
        amount_remaining=round(loan_info.amount + repayment.amount_remaining_change, 4),
        remaining_duration=loan_info.remaining_duration - 1,
    )


def create_monthly_repayment(loan_info: LoanInfo) -> MonthlyRepayment:
    fixed_interest = FixedInterestStrategy()
    variable_interest = VariableInterestStrategy(loan_info.libor)
    default_strategy = InterestAndRepaymentStrategy(fixed_interest)
    repayment_strategy: RepaymentStrategyABC = {
        "interest_only": InterestOnlyRepaymentStrategy(fixed_interest),
        "interest_only_variable": InterestOnlyRepaymentStrategy(variable_interest),
        "interest_and_repayment": InterestAndRepaymentStrategy(fixed_interest),
        "v_interest_and_repayment": InterestAndRepaymentStrategy(variable_interest),
        "introductory_offer_3": IntroductoryOfferRepaymentStrategy(fixed_interest, 3),
        "introductory_offer_12": IntroductoryOfferRepaymentStrategy(variable_interest, 12),
        "introductory_offer_interst_only_6": IntroductoryInterestOnlyOfferRepaymentStrategy(fixed_interest, 6),
        "introductory_offer_interst_only_9": IntroductoryInterestOnlyOfferRepaymentStrategy(fixed_interest, 9),
        "good_credit_score": GoodCreditScoreRepaymentStrategy(fixed_interest, 700),
        "very_good_credit_score": GoodCreditScoreRepaymentStrategy(variable_interest, 850),
        "bad_credit_score": BadCreditScoreRepaymentStrategy(fixed_interest, 650),
        "very_bad_credit_score": BadCreditScoreRepaymentStrategy(fixed_interest, 500),
        # TODO: add actual solutions
    }.get(loan_info.loan_kind, default_strategy)

    return calculate_repayment(loan_info, repayment_strategy)


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
