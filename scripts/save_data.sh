#!/usr/bin/env bash
# שומר את data/ בחזרה לריפו. עמיד להתנגשויות (הרצה חוזרת מקומיט ישן, שני סשנים) ולנפילות רשת רגעיות.
set -u
MSG="${1:-data update}"
git config user.name "newsbot"
git config user.email "newsbot@users.noreply.github.com"
git add data
git commit -m "$MSG [skip ci]" || exit 0
for i in 1 2 3 4 5; do
  if git pull --rebase -X theirs && git push; then exit 0; fi
  echo "save attempt $i failed - retrying"
  git rebase --abort 2>/dev/null || true
  sleep $((i * 4))
done
# מוצא אחרון: דוחפים בלי למזג, כדי לא לאבד את היומן (הגרסה המקומית מנצחת)
git fetch origin main && git reset --soft origin/main && git commit -m "$MSG (forced merge) [skip ci]" && git push
