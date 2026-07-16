type VercelRequest = {
  method?: string;
  body?: { message?: unknown; alcohol?: unknown; theme?: unknown; themeDescription?: unknown };
};
type VercelResponse = {
  status: (code: number) => VercelResponse;
  json: (body: unknown) => unknown;
};
declare const process: { env: Record<string, string | undefined> };

const json = (res: VercelResponse, status: number, body: unknown) =>
  res.status(status).json(body);

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== "POST") return json(res, 405, { error: "POST 요청만 허용됩니다." });

  const message = typeof req.body?.message === "string" ? req.body.message.trim() : "";
  const alcohol = typeof req.body?.alcohol === "string" ? req.body.alcohol : "주류";
  const theme = typeof req.body?.theme === "string" ? req.body.theme : "현재 선택된 무드";
  const themeDescription = typeof req.body?.themeDescription === "string" ? req.body.themeDescription : "";
  if (!message) return json(res, 400, { error: "message 입력이 필요합니다." });
  if (message.length > 200) return json(res, 400, { error: "message는 200자 이하로 입력해 주세요." });
  if (!process.env.OPENAI_API_KEY) return json(res, 503, { error: "OPENAI_API_KEY가 설정되지 않았습니다." });

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: process.env.OPENAI_MODEL || "gpt-5-mini",
        response_format: { type: "json_object" },
        messages: [
          {
            role: "system",
            content:
              '사용자의 한국어 입력에서 핵심 분위기와 상황을 파악하고, 선택된 무드와 어울리는 칵테일 추천 화면의 짧은 감성 문구로 바꾸세요. JSON만 반환하세요. 키는 "moodLabel", "moodDescription"입니다. moodLabel은 2~10자 정도의 자연스러운 형용사 표현(예: 달콤하고 설레는, 차분하고 느린)으로 작성하세요. moodDescription은 원문을 복사하거나 인용하지 말고, 입력의 특정 단어와 상황을 자연스럽게 반영해 새롭게 작성하세요. "라는 마음에 어울리는" 같은 기계적인 표현은 사용하지 마세요. 선택된 무드가 Flirt라면 설렘·데이트·달콤함을, Soft Mood라면 포근함·편안함·휴식을, Rainy Day라면 비·차분함·위로를 우선 반영하세요. 주종은 문구에 넣지 마세요.',
          },
          {
            role: "user",
            content: `사용자 입력: ${message}\n선택된 무드: ${theme}\n무드 설명: ${themeDescription}\n추천 주종 참고: ${alcohol}`,
          },
        ],
      }),
    });
    if (!response.ok) throw new Error(`OpenAI request failed: ${response.status}`);
    const body = (await response.json()) as { choices?: Array<{ message?: { content?: string } }> };
    const content = body.choices?.[0]?.message?.content;
    if (!content) throw new Error("문구 응답이 없습니다.");
    const copy = JSON.parse(content) as { moodLabel?: unknown; moodDescription?: unknown };
    if (typeof copy.moodLabel !== "string" || typeof copy.moodDescription !== "string") {
      throw new Error("문구 형식이 올바르지 않습니다.");
    }
    return json(res, 200, {
      moodLabel: copy.moodLabel.trim(),
      moodDescription: copy.moodDescription.trim(),
    });
  } catch {
    return json(res, 502, { error: "AI 문구 생성에 실패했습니다." });
  }
}
