#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# GitHub Actions ↔ 구글 "키 없는 인증" 설정 (Google Cloud Shell 에 붙여 넣어 실행)
# 서비스 계정 키(JSON)를 만들 수 없는 조직 정책에서도 동작합니다.
# 여러 번 실행해도 안전합니다(이미 있으면 건너뜀).
# ─────────────────────────────────────────────────────────────
set -e
REPO="Jaeyeol8712/Transtool"
SA_NAME="aroundtool-bot"
PROJECT_ID="$(gcloud config get-value project 2>/dev/null)"
[ -z "$PROJECT_ID" ] && { echo "먼저 위쪽에서 프로젝트를 선택하세요: gcloud config set project 프로젝트ID"; exit 1; }
PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"
SA="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

echo "▶ API 사용 설정"
gcloud services enable iamcredentials.googleapis.com sts.googleapis.com \
  searchconsole.googleapis.com analyticsdata.googleapis.com --quiet

echo "▶ 서비스 계정 확인"
gcloud iam service-accounts describe "$SA" >/dev/null 2>&1 || \
  gcloud iam service-accounts create "$SA_NAME" --display-name="aroundtool bot"

echo "▶ GitHub 연결용 풀·공급자"
gcloud iam workload-identity-pools describe github --location=global >/dev/null 2>&1 || \
  gcloud iam workload-identity-pools create github --location=global --display-name="GitHub Actions"
gcloud iam workload-identity-pools providers describe transtool --location=global --workload-identity-pool=github >/dev/null 2>&1 || \
  gcloud iam workload-identity-pools providers create-oidc transtool --location=global \
    --workload-identity-pool=github --display-name="Transtool" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
    --attribute-condition="assertion.repository=='$REPO'"

echo "▶ 이 저장소만 서비스 계정을 쓸 수 있게 허용"
gcloud iam service-accounts add-iam-policy-binding "$SA" --quiet \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github/attribute.repository/$REPO" >/dev/null

echo
echo "════════ 완료 — 아래 두 값을 GitHub Variables 에 등록하세요 ════════"
echo "GCP_WIF_PROVIDER    = projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github/providers/transtool"
echo "GCP_SERVICE_ACCOUNT = $SA"
echo
echo "서치콘솔(전체 권한)·GA4(뷰어)에 추가할 이메일: $SA"
