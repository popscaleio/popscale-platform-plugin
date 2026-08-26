# Usage Metric Semantics

## Journey current state

Journey insights are a current-state view, not an “as of” historical snapshot.

- Participation rate is enrolled members with `started_at` divided by enrolled
  members.
- Completion rate is currently completed members divided by enrolled members.
- Average mastery is the mean of available current Journey mastery values.
- The privacy cohort is active enrolled members contributing to that group, not
  every company member assigned to the department.
- Department and role grouping use each membership's current stored values.

State those semantics when the wording “historically”, “at the time”, or an
organizational reorganization could change the interpretation.

## Content attempts

An evaluated attempt depends on its format:

- Roleplay and Coaching Session: evaluation finished and an evaluation score
  exists.
- Episode: consumed duration is positive and a normalized outcome can be
  determined.
- Challenge: a final pass/no-pass result exists.
- Flashcard Deck: the session is complete and a knew-score can be determined.

`average_outcome_pct` is the mean normalized outcome for evaluated attempts.
`pass_rate_pct` uses only attempts with a determinable pass value; direct
attempts without a Journey threshold are excluded from that denominator.
Report those denominators rather than treating all attempts as evaluated or
pass-eligible.

## Historical score contract

- Roleplay and Coaching history normalizes saved scores using the content's
  current maximum. A linked pass result uses the current Journey-item threshold.
- Flashcard sessions retain attempt card counts, but linked pass results still
  use the current Journey-item threshold.
- Modern Episode attempts use immutable outcome inputs. Legacy attempts without
  those snapshots can fall back to current media or Journey configuration.
- Challenge pass/no-pass is stored on the attempt.

Keep the response's `score_contract` or `historical_score_notice` beside these
metrics. Prefer wording such as “reported under the current scoring/threshold
contract” over “the learner scored exactly this at the time.” Do not invent a
historical correction or combine current configuration with outside data.
