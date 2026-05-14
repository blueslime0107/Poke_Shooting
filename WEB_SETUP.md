# Poke_Shooting 웹 빌드 실행 가이드

## 문제 상황
Codespaces + Live Server에서 pygbag 게임 로드 실패:
```
Access to fetch ... has been blocked by CORS policy
Failed to load resource: net::ERR_FAILED
```

**원인**: 포트가 Private일 때 인증 리다이렉트 발생 → CORS 차단

---

## ✅ 해결 방법 (2가지)

### 방법 1️⃣: 포트를 Public으로 변경 (추천)
**가장 간단합니다.**

1. **Codespaces 포트 탭 열기**
   - VS Code 하단의 "포트" 탭 클릭
   - 또는 Command Palette → "Ports: Focus on Ports View"

2. **5500 포트를 Public으로 변경**
   - 포트 목록에서 5500 우클릭
   - "포트 공개 상태 변경" → **Public** 선택
   - ![port-public](https://imgur.com/a1b2c3d.png)

3. **Live Server로 index.html 열기**
   - VS Code에서 `/build/web/index.html` 우클릭
   - "Open with Live Server" 선택
   - 또는 Command Palette → "Live Server: Open with Live Server"

✓ 포트가 Public이면 인증 리다이렉트 없음 → 게임 로드됨

---

### 방법 2️⃣: CORS 헤더가 있는 Python 서버 사용
**프로젝트 스크립트로 자동 실행**

```bash
# 터미널에서 실행
cd /workspaces/Poke_Shooting
python3 serve_web_cors.py
```

그 다음:
- 브라우저에서 `http://localhost:8000` 접속
- 또는 VS Code에서 "Remote: Open in Browser" → localhost:8000 입력

✓ CORS 헤더 자동 추가 → Private 포트도 동작

---

## 🔍 어느 방법을 써야 하나?

| 상황 | 추천 방법 |
|------|---------|
| 빠른 테스트 원할 때 | **방법 1** (포트 Public) |
| 포트 노출이 싫을 때 | **방법 2** (CORS 서버) |
| 프로덕션 배포할 때 | 호스팅 서비스 사용 |

---

## 📋 체크리스트

- [ ] 방법 1 또는 2 선택
- [ ] Live Server 또는 CORS 서버 실행
- [ ] 브라우저에서 페이지 **하드 새로고침** (Ctrl+Shift+R 또는 Cmd+Shift+R)
- [ ] 콘솔에서 "Ready to start! Please click/touch page" 메시지 확인
- [ ] 화면에 클릭/터치 → 게임 시작

---

## 🐛 여전히 안 되면

```bash
# 브라우저 DevTools 열기 (F12)
# Console 탭에서 다음 확인:

# 1. 콘솔 오류 메시지 전문 복사
# 2. 포트가 Public인지 확인
# 3. 브라우저 캐시 완전 삭제 후 재시도
```

---

## 기술 상세 (선택사항)

**왜 이 문제가 발생하나?**
- Codespaces Private 포트 = 접근 시 인증 페이지로 리다이렉트
- pygbag의 `platform.fopen()` = HTTP fetch 사용 (자동 인증 불가)
- fetch의 CORS 정책 = 교차 출처 리다이렉트 차단

**수정된 코드:**
- [build/web/index.html](../build/web/index.html) - apk/tar.gz 폴백 로직 추가
- [serve_web_cors.py](../serve_web_cors.py) - CORS 헤더 Python 서버
