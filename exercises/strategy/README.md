# Strategy Pattern

The Strategy Pattern is a Behavioural pattern first published in the Gang of Four book _Design Patterns: Elements of Reusable Object-Oriented Software_.

TODO: Write about the use cases of this pattern; In the meantime, read about the [Strategy Pattern on Wikipedia](https://en.wikipedia.org/wiki/Strategy_pattern)

## Strategy Pattern Exercise

In this exercise, you are implementing a bank's fixed length loan interest calculation. There is legacy code already in place, that supports a number of different interest repayments, including past offers. It is passed an object of a specific kind, and must return a specific object, which contains the relevant info for a monthly repayment. You are not allowed to modify the signature of the method or the objects passed in (or you can, but it makes the exercise less interesting...)

### Requirements

The input object `LoanInfo` has the following fields:

 - `loan_id`: This is a unique ID for the loan
 - `loan_kind`: Determins how the loan is repaid. See list of loan kinds further down
 - `original_duration`: How many months the loan is for originally
 - `remaining_duration`: How many months remain for the loan. When it equals `original_duration` that is the first month's repayment. When it is 1, that is the last repayment
 - `interest`: The % interest to be paid for this loan. E.g.: if it's 5.0, it's 5% interest
 - `amount`: The amount remaining to be repaid for the loan
 - `current_credit_score`: The current credit score of the user who's loan it is
 - `libor`: The interest rate banks offer each other. This is used in flexible interest calculations

You must return a `MonthlyRepayment` with the following fields:

 - `loan_id`: This is the unique ID for the loan, same as the `LoanInfo`
 - `payment`: The amount to be repaid this month, rounded to 4 decimal places
 - `amount_remaining`: The amount remaining of the loan, after the repayment, rounded to 4 decimal places
 - `remaining_duration`: The duration remaining of the loan

Variable rate interest is calculated as `libor + interest`. Interest for a given month is calculated as 1/12 of the annual interest: `1 / 12`.

The different loan kinds available (they are named inconsistently, for legacy reasons):

 - `interest_only`: The user only repays the fixed interest each month, except the last repayment, where they repay interest plus the full loan amount
 - `interest_only_variable`: Same as `interest_only`, but the user pays a variable interest
 - `interest_and_repayment`: Each month the user repays the interest for the remaining amount plus an equal portion of the remaning amount
 - `v_interest_and_repayment`: Same as `interest_and_repayment`, but the user pays a variable interest
 - `introductory_offer_3`: In this introductory offer, the user doesn't pay anything for the first 3 months. These always have a duration longer than 6 months (you don't have to validate this). The user does acrew interest during this time however. After that, they repay at a fixed rate same as `interest_and_repayment`
 - `introductory_offer_12`: In this offer the user doesn't pay anything for 12 months (but does acrew interest). After that, they repay at a flexible rate, same as `v_interest_and_repayment`. (These are always at least 24 months in duration)
 - `introductory_offer_interest_only_6`: In this offer, the user only pays interest for the first 6 months, then they start repaying at a fixed rate, same as `interest_and_repayment` (minimum duration 12 months)
 - `introductory_offer_interest_only_9`: Same as `introductory_offer_interest_only_6` but with a 9 month initial period (and minimum duration of 18 months)
 - `good_credit_score`: This is the same as a `interest_and_repayment`, but if in a given month, a user has a credit score of at least 700, they don't pay or acrew any interest.
 - `very_good_credit_score`: Similar to `good_credit_score`, but it's offered for at a variable rate, and the user must have a credit score of at least 850
 - `bad_credit_score`: similar to `good_credit_score`, this is an `interest_and_repayment` loan, but if the user has a credit score worse than 650, they must pay double the interest that month
 - `very_bad_credit_score`: same as a `bad_credit_score`, but only double if the user has a credit score worse than 500

### Your goals are

You are tasked with adding the following new credit scores:

 - `introductory_offer_6`: Same as `introductory_offer_3`, meaning no repayment for 6 months, fixed interest rate.
 - `interest_and_repayment_min_variable`: Same as `interest_and_repayment`, but interest is calculated as `libor + 1%`, unless libor is under `interest`, at which point it is calculated as `interest`
 - `interest_only_min_variable`: Same as `interest_and_repayment_min_variable`, but only the interest is paid each month.
 - `credit_score_variable`: Similar to the other credit score kinds, but here, if the credit score is less than 500, 2% additional interest is added; if it's less than 650, 1% additional interest is added and if it's more than 750, interest is reduced by 0.5% (interest cannot be less than 0.1%)

As you see, given that the loan kind can change often, this use case is well suited for restructuring using the Strategy Pattern. Consider adding tests for the different cases overall. Also consider how you could test just the interest rate calculations, and just the repayment calculations separately.

### Hints

<details>
  <summary>Hint 1</summary>

There are two candidates at the application of the strategy pattern: The interest rate calculation, and the repayment calculation. You can refactor either, or even both!

</details>

<details>
  <summary>Hint 2</summary>

Both for the different positive or negative credit score calculations, or the two different introductory offer calculations, you could create a strategy each, parameterised by the interest strategy and the credit score threshold or offer period.

</details>

<details>
  <summary>Hint 3</summary>

When two stategies are quite similar, you can inherit the more basic one, and add more complexity. Such as for introductory offers, you can calculate the repayment and change in amount remaining separate during the offer period, then fall back to the interest and repayment strategy

</details>