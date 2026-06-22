<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Komorebi Log - 莫蘭迪日系手帳</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Noto Sans TC', sans-serif;
    }
    /* 隱藏滾動條但保持功能 */
    .scrollbar-none::-webkit-scrollbar {
      display: none;
    }
    .scrollbar-none {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
  </style>
</head>
<body>

  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect, useRef } = React;

    // ==========================================
    // 1. 主題配色定義
    // ==========================================
    const THEMES = {
      matcha: {
        name: "夏日抹茶 (Matcha)",
        bg: "#FAF6F0",
        primary: "#8C9E86",
        secondary: "#DCAE96",
        neutral: "#4E423E",
        card: "#F3EDE2",
        accent: "#92A3A8",
        accentBg: "#E2EDE4",
        borderColor: "#E5DDD0",
      },
      sakura: {
        name: "春櫻爛漫 (Sakura)",
        bg: "#FFFBF9",
        primary: "#E09F9E",
        secondary: "#D1A58E",
        neutral: "#5C4E4B",
        card: "#FBF1EF",
        accent: "#A5B8A1",
        accentBg: "#F6ECEB",
        borderColor: "#EADAD8",
      },
      chestnut: {
        name: "秋山栗褐 (Chestnut)",
        bg: "#FAF5EF",
        primary: "#B38E6F",
        secondary: "#856E5F",
        neutral: "#453C37",
        card: "#F2EAE0",
        accent: "#8A9684",
        accentBg: "#ECF2E6",
        borderColor: "#DFD2C4",
      },
      snowy: {
        name: "冬雪靜謐 (Snowy)",
        bg: "#F5F8F9",
        primary: "#8FAAB3",
        secondary: "#BDB3A6",
        neutral: "#3A4145",
        card: "#EDF2F4",
        accent: "#D4AA94",
        accentBg: "#E5ECEF",
        borderColor: "#D2DFE2",
      }
    };

    // ==========================================
    // 2. 御神籤幸運籤詩資料庫
    // ==========================================
    const fortunesList = [
      { rank: "✨ 大吉 大安", title: "健康與美麗之神眷顧著你！", tip: "今天體力充沛，非常適合挑戰稍微重一點的負重練習。幸運食物是烤鯖魚，多喝一杯抹茶會帶來滿滿活力唷！🌸" },
      { rank: "🌱 中吉 吉日", title: "溫柔的小草正在快樂發芽", tip: "今天只要專注做好核心訓練，哪怕只練10分鐘也極具收穫。幸運顏色是大地綠，多補充天然大豆製品吧！" },
      { rank: "🍊 小吉 溫暖", title: "放慢腳步，也是一種修行", tip: "今天不需要把自己逼得太緊。做做平板支撐、拉拉筋，保持呼吸。多喝一杯暖胃的味噌湯吧！" },
      { rank: "🌻 吉 迎風", title: "迎著微風，今天會是收穫滿滿的一天！", tip: "優質的蛋白質正在好好的修補肌肉呢。晚上記得睡個好覺，明天的健康指數會翻倍哦！" },
      { rank: "🍂 半吉 靜心", title: "靜心聆聽，身體渴望水分的聲音", tip: "今天適合多喝水與補充膳食纖維。安排 15 分鐘的瑜珈或溫和伸展，讓關節與心靈得到極致的放鬆吧。" },
      { rank: "🌾 末吉 微笑", title: "微微笑，今天也是踏實的一步", tip: "不要跟別人比較進度。今天只要多走 2000 步，或者提早 30 分鐘上床睡覺，就是對身體最溫柔的愛護護理！" }
    ];

    function App() {
      // --- 基礎系統與主題設定 ---
      const [currentThemeKey, setCurrentThemeKey] = useState('matcha');
      const theme = THEMES[currentThemeKey];

      const [activeTab, setActiveTab] = useState('diary'); 
      const [selectedDay, setSelectedDay] = useState('Mon'); 

      // --- 1. 寵物「小嫩芽」養成狀態 ---
      const [petExp, setPetExp] = useState(20); 
      const [petStage, setPetStage] = useState(1); // 1: 種子, 2: 嫩芽, 3: 花苞, 4: 盛開
      const [petName, setPetName] = useState("綠綠子");
      const [isEditingPetName, setIsEditingPetName] = useState(false);
      const [petActionMessage, setPetActionMessage] = useState("今天也要好好補充水分跟蛋白質唷 🌱");

      // --- 2. 每日抽卡「御神籤」狀態 ---
      const [hasDrawnFortune, setHasDrawnFortune] = useState(false);
      const [drawnFortune, setDrawnFortune] = useState(null);
      const [showFortuneModal, setShowFortuneModal] = useState(false);

      // --- 3. 水分追蹤 (Hydration) ---
      const [waterCups, setWaterCups] = useState({
        Mon: 3, Tue: 0, Wed: 0, Thu: 0, Fri: 0, Sat: 0, Sun: 0
      });

      // --- 4. 電子手寫風貼紙簿 ---
      const availableStickers = ["🔋", "💦", "💮", "🍵", "🏃‍♀️", "🍌", "💯", "😴", "🍰", "🍙"];
      const [placedStickers, setPlacedStickers] = useState({
        Mon: ["💮", "🍵"], Tue: [], Wed: [], Thu: [], Fri: [], Sat: [], Sun: []
      });

      // --- 5. 實體蓋章打卡牆數據 ---
      const [stampedDays, setStampedDays] = useState({
        Mon: true, Tue: false, Wed: false, Thu: false, Fri: false, Sat: false, Sun: false
      });
      const [showStampSuccess, setShowStampSuccess] = useState(false);

      // --- 6. AI 魔法輸入狀態 ---
      const [aiInputText, setAiInputText] = useState('');
      const [aiLoading, setAiLoading] = useState(false);
      const [aiError, setAiError] = useState(null);

      // --- 7. 番茄休息計時器狀態 ---
      const [timerSeconds, setTimerSeconds] = useState(60); 
      const [timerActive, setTimerActive] = useState(false);
      const [timerPreset, setTimerPreset] = useState(60); 
      const timerRef = useRef(null);

      // --- 8. 飲食與健身資料庫 ---
      const [meals, setMeals] = useState({
        Mon: [
          { id: 1, name: '烤雞胸肉便當', calories: 510, protein: 42 },
          { id: 2, name: '無糖高纖豆漿', calories: 130, protein: 12 },
        ],
        Tue: [], Wed: [], Thu: [], Fri: [], Sat: [], Sun: []
      });

      const [newMealName, setNewMealName] = useState('');
      const [newMealCalories, setNewMealCalories] = useState('');
      const [newMealProtein, setNewMealProtein] = useState('');

      const [weeklyWorkouts, setWeeklyWorkouts] = useState({
        Mon: [1, 3], Tue: [2], Wed: [4, 5], Thu: [], Fri: [1], Sat: [], Sun: []
      });

      const [exercisesDatabase, setExercisesDatabase] = useState([
        {
          id: 1,
          name: '相撲深蹲 (Sumo Squat)',
          category: '腿部臀部',
          level: '入門',
          tags: ['股四頭肌', '內收肌群', '臀大肌'],
          description: '雙腳站距寬於肩膀，腳尖朝外約45度，雙手握拳於胸前，下蹲至大腿與地面平行。',
          tips: '下蹲時膝蓋保持與腳尖方向一致，核心收緊，背部挺直。',
          breathing: '吸氣下蹲，呼氣時用臀部及大腿力量站起。',
          svgPath: (color) => (
            <svg viewBox="0 0 100 100" className="w-16 h-16 stroke-current fill-none" style={{ color }} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="50" cy="20" r="7" />
              <path d="M50 27 L50 48" />
              <path d="M50 32 L35 38 L50 44 L65 38 Z" fill="#FAF6F0" />
              <path d="M50 48 L32 58 L24 78" />
              <path d="M50 48 L68 58 L76 78" />
              <path d="M20 78 H28 M72 78 H80" />
            </svg>
          )
        },
        {
          id: 2,
          name: '滑輪下拉 (Lat Pulldown)',
          category: '背部肌群',
          level: '進階',
          tags: ['闊背肌', '大圓肌', '二頭肌'],
          description: '端坐在拉背機前，雙手寬握把手。挺胸收腹，利用背肌力量將把手往下拉至鎖骨上方。',
          tips: '避免用身體往後傾倒借力，感受肩膀往下壓、肩膀夾緊的感覺。',
          breathing: '向下拉時吐氣，控制回放時吸氣。',
          svgPath: (color) => (
            <svg viewBox="0 0 100 100" className="w-16 h-16 stroke-current fill-none" style={{ color }} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 15 H80" strokeWidth="4" />
              <path d="M50 15 L50 20 M32 15 L38 32 M68 15 L62 32" strokeDasharray="2 2" />
              <circle cx="50" cy="35" r="7" />
              <path d="M50 42 L50 65" />
              <path d="M38 32 L50 44 L62 32" />
              <path d="M40 65 H60 M45 65 L40 85 M55 65 L60 85" />
            </svg>
          )
        },
        {
          id: 3,
          name: '伏地挺身 (Push-Up)',
          category: '胸肌與核心',
          level: '中階',
          tags: ['胸大肌', '前三角肌', '三頭肌'],
          description: '雙手打開略寬於肩撐地，身體呈一直線。屈肘向下壓至胸部接近地面，再推回起始位置。',
          tips: '護腰核心要鎖死，臀部不要往下塌陷或往上拱起。',
          breathing: '身體下壓時吸氣，向上推起時吐氣。',
          svgPath: (color) => (
            <svg viewBox="0 0 100 100" className="w-16 h-16 stroke-current fill-none" style={{ color }} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="80" cy="35" r="6" />
              <path d="M74 38 L25 58" />
              <path d="M65 42 L65 65" />
              <path d="M25 58 L22 65" />
              <path d="M15 65 H85" strokeWidth="1" strokeDasharray="3 3" />
            </svg>
          )
        },
        {
          id: 4,
          name: '啞鈴側平舉 (Lateral Raise)',
          category: '肩部雕塑',
          level: '入門',
          tags: ['三角肌中束', '斜方肌'],
          description: '雙手各持一啞鈴垂於身體兩側。手肘微彎，向身體兩側抬起啞鈴，至雙手與肩膀平行。',
          tips: '抬起時手肘維持微彎，小拇指微往上轉，感受肩外側擠壓。',
          breathing: '抬起時吐氣，緩慢放下時吸氣。',
          svgPath: (color) => (
            <svg viewBox="0 0 100 100" className="w-16 h-16 stroke-current fill-none" style={{ color }} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="50" cy="22" r="7" />
              <path d="M50 29 L50 55" />
              <path d="M50 55 L40 80 M50 55 L60 80" />
              <path d="M25 35 H75" />
              <circle cx="22" cy="35" r="4" fill="currentColor" />
              <circle cx="78" cy="35" r="4" fill="currentColor" />
            </svg>
          )
        }
      ]);

      const [customExName, setCustomExName] = useState('');
      const [customExCategory, setCustomExCategory] = useState('核心穩定');
      const [customExTips, setCustomExTips] = useState('');
      const [showCustomExModal, setShowCustomExModal] = useState(false);
      const [activeExerciseDetail, setActiveExerciseDetail] = useState(null);
      const [assigningExercise, setAssigningExercise] = useState(null);

      const CALORIE_LIMIT = 1200;
      const PROTEIN_LIMIT = 80;

      const currentDayMeals = meals[selectedDay] || [];
      const totalCalories = currentDayMeals.reduce((sum, item) => sum + item.calories, 0);
      const totalProtein = currentDayMeals.reduce((sum, item) => sum + item.protein, 0);

      // --- 計時器邏輯 ---
      useEffect(() => {
        if (timerActive && timerSeconds > 0) {
          timerRef.current = setInterval(() => {
            setTimerSeconds(prev => prev - 1);
          }, 1000);
        } else if (timerSeconds === 0) {
          setTimerActive(false);
          clearInterval(timerRef.current);
          setPetActionMessage("⏱️ 叮咚！休息結束！快起來補水準備下一組動作囉！🌻");
        }
        return () => clearInterval(timerRef.current);
      }, [timerActive, timerSeconds]);

      // --- 寵物升級邏輯 ---
      useEffect(() => {
        if (petExp >= 100) {
          if (petStage < 4) {
            setPetStage(prev => prev + 1);
            setPetExp(10);
            setPetActionMessage(`🎉 哇！太棒了！${petName} 順利進化囉！離健康盛開更近一步！`);
          } else {
            setPetExp(100);
          }
        }
      }, [petExp]);

      const rewardPet = (amount, reason) => {
        setPetExp(prev => Math.min(prev + amount, 100));
        setPetActionMessage(`✨ ${reason}！${petName} 開心地吸收了能量 (+${amount} 經驗值)`);
      };

      const drawFortune = (isReDraw = false) => {
        if (hasDrawnFortune && !isReDraw) {
          setShowFortuneModal(true);
          return;
        }
        const randomIndex = Math.floor(Math.random() * fortunesList.length);
        setDrawnFortune(fortunesList[randomIndex]);
        setHasDrawnFortune(true);
        setShowFortuneModal(true);
        rewardPet(15, isReDraw ? "重新求取了幸運手帳籤" : "抽取了今日健康籤詩");
      };

      // --- 模擬 AI 輸入 (因為前端沒有金鑰，改為智能模擬解析，防呆且流暢) ---
      const handleAiInputSubmit = (e) => {
        e.preventDefault();
        if (!aiInputText.trim()) return;

        setAiLoading(true);
        setAiError(null);

        setTimeout(() => {
          let guessedName = aiInputText.substring(0, 10);
          let guessedCal = Math.floor(Math.random() * 300) + 150;
          let guessedProtein = Math.floor(Math.random() * 20) + 10;

          // 簡單匹配常見關鍵字讓模擬更有魔法感
          if(aiInputText.includes("雞肉") || aiInputText.includes("雞胸")) { guessedCal = 280; guessedProtein = 35; }
          else if(aiInputText.includes("蛋")) { guessedCal = 140; guessedProtein = 14; }
          else if(aiInputText.includes("優格")) { guessedCal = 120; guessedProtein = 10; }
          else if(aiInputText.includes("豆漿")) { guessedCal = 130; guessedProtein = 12; }

          const newMeal = {
            id: Date.now(),
            name: `[AI智慧估算] ${aiInputText}`,
            calories: guessedCal,
            protein: guessedProtein
          };

          setMeals(prev => ({
            ...prev,
            [selectedDay]: [...(prev[selectedDay] || []), newMeal]
          }));

          setAiInputText('');
          setAiLoading(false);
          rewardPet(20, "使用 AI 魔法記錄了健康飲食");
        }, 1000);
      };

      const handleAddMeal = (e) => {
        e.preventDefault();
        if (!newMealName || !newMealCalories || !newMealProtein) return;

        const newMeal = {
          id: Date.now(),
          name: newMealName,
          calories: parseInt(newMealCalories),
          protein: parseInt(newMealProtein)
        };

        setMeals(prev => ({
          ...prev,
          [selectedDay]: [...(prev[selectedDay] || []), newMeal]
        }));

        setNewMealName('');
        setNewMealCalories('');
        setNewMealProtein('');
        rewardPet(10, "新增了一筆美味紀錄");
      };

      const handleDeleteMeal = (mealId) => {
        setMeals(prev => ({
          ...prev,
          [selectedDay]: prev[selectedDay].filter(m => m.id !== mealId)
        }));
      };

      const handleDrinkWater = () => {
        setWaterCups(prev => {
          const current = prev[selectedDay] || 0;
          if (current >= 8) return prev; 
          return { ...prev, [selectedDay]: current + 1 };
        });
        rewardPet(15, "喝了一大杯乾淨的水");
      };

      const handleApplySticker = (sticker) => {
        setPlacedStickers(prev => {
          const current = prev[selectedDay] || [];
          if (current.includes(sticker)) return prev;
          return { ...prev, [selectedDay]: [...current, sticker] };
        });
        rewardPet(5, "裝飾了今天的療癒手帳");
      };

      const handleRemoveSticker = (sticker) => {
        setPlacedStickers(prev => ({
          ...prev,
          [selectedDay]: prev[selectedDay].filter(s => s !== sticker)
        }));
      };

      const handleStampCheckin = () => {
        setStampedDays(prev => ({ ...prev, [selectedDay]: true }));
        setShowStampSuccess(true);
        rewardPet(30, "完成了今日手帳健康打卡結算");
        setTimeout(() => { setShowStampSuccess(false); }, 2500);
      };

      const handleAddCustomExercise = (e) => {
        e.preventDefault();
        if (!customExName) return;

        const newEx = {
          id: Date.now(),
          name: `${customExName} (自訂)`,
          category: customExCategory,
          level: '入門',
          tags: ['自主訓練', '自定義'],
          description: '這是您自訂的個人化動作說明。',
          tips: customExTips || '無特殊技巧，保持正確姿勢。',
          breathing: '動作時保持規律呼吸，切勿憋氣。',
          svgPath: (color) => (
            <svg viewBox="0 0 100 100" className="w-16 h-16 stroke-current fill-none" style={{ color }} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="50" cy="20" r="10" />
              <path d="M50 30 L50 60 M50 60 L30 85 M50 60 L70 85 M20 40 L80 40" />
            </svg>
          )
        };

        setExercisesDatabase(prev => [newEx, ...prev]);
        setCustomExName('');
        setCustomExTips('');
        setShowCustomExModal(false);
        rewardPet(15, "新增了專屬動作卡片");
      };

      // 拖曳編排支援
      const handleDragStart = (e, exerciseId) => { e.dataTransfer.setData("text/plain", exerciseId); };
      const handleDragOver = (e) => { e.preventDefault(); };
      const handleDrop = (e, targetDay) => {
        e.preventDefault();
        const exerciseId = parseInt(e.dataTransfer.getData("text/plain"));
        if (exerciseId) addExerciseToDay(exerciseId, targetDay);
      };

      const addExerciseToDay = (exerciseId, day) => {
        setWeeklyWorkouts(prev => {
          const currentList = prev[day] || [];
          if (currentList.includes(exerciseId)) return prev;
          return { ...prev, [day]: [...currentList, exerciseId] };
        });
        rewardPet(10, `指派了動作至週計劃`);
      };

      const removeExerciseFromDay = (exerciseId, day) => {
        setWeeklyWorkouts(prev => ({
          ...prev,
          [day]: (prev[day] || []).filter(id => id !== exerciseId)
        }));
      };

      const getMotivationalFeedback = () => {
        if (currentDayMeals.length === 0) {
          return { text: "寫下你的第一筆飲食紀錄吧！今天的目標是 1200 kcal、80g 蛋白質，讓我們一步步輕鬆達成 ☕️" };
        }
        if (totalCalories >= 1100 && totalCalories <= 1300 && totalProtein >= PROTEIN_LIMIT) {
          return { text: "「恭喜你！」今天的熱量與蛋白質掌握得無懈可擊，簡直是完美的健康範本！為認真自己蓋個章吧 💮" };
        }
        if (totalCalories > 1300) {
          return { text: "熱量今天稍微超標了一點點，但沒關係的！身體正在好好的代謝呢。明天我們再一起溫柔地調整節奏吧 ✨" };
        }
        return { text: `今天已經補充了 ${totalCalories} 大卡及 ${totalProtein}g 蛋白質。再接再厲，你做得很好喔 🧸` };
      };

      const feedback = getMotivationalFeedback();

      const getNextMealRecommendations = () => {
        const remainingKcal = CALORIE_LIMIT - totalCalories;
        if (remainingKcal <= 100) {
          return [
            { name: "無糖黑咖啡 / 麥茶", kcal: 5, desc: "幾乎零熱量，適合飽腹且想轉換心情時飲用。" },
            { name: "和風輕卡蒟蒻條", kcal: 35, desc: "高纖低卡，滿足口腹之慾。" }
          ];
        }
        return [
          { name: "舒肥雞胸肉佐溏心蛋沙拉", kcal: 320, desc: "清爽無負擔，雙重優質蛋白質補好補滿！" },
          { name: "昆布柴魚豆腐蔬菜湯", kcal: 180, desc: "暖胃首選，植物性大豆蛋白與豐富膳食纖維。" }
        ];
      };

      const recommendations = getNextMealRecommendations();

      const dayNameMapping = {
        Mon: { short: '週一', long: '星期一' },
        Tue: { short: '週二', long: '星期二' },
        Wed: { short: '週三', long: '星期三' },
        Thu: { short: '週四', long: '星期四' },
        Fri: { short: '週五', long: '星期五' },
        Sat: { short: '週六', long: '星期六' },
        Sun: { short: '週日', long: '星期日' }
      };

      return (
        <div className="min-h-screen flex justify-center pb-24 transition-colors duration-500" style={{ backgroundColor: theme.bg, color: theme.neutral }}>
          <div className="w-full max-w-md min-h-screen flex flex-col shadow-2xl border-x relative overflow-hidden transition-all duration-300" 
               style={{ borderColor: theme.borderColor, backgroundColor: theme.bg }}>
            
            {/* 活頁本頂部孔飾 */}
            <div className="w-full h-4 bg-gradient-to-r from-red-100 via-yellow-100 to-blue-100 flex justify-between px-6 items-center">
              {[...Array(8)].map((_, i) => <div key={i} className="w-2.5 h-2.5 rounded-full bg-stone-300/60 shadow-inner -mt-1" />)}
            </div>

            {/* 紙膠帶裝飾條 */}
            <div className="h-6 w-full opacity-90 relative flex items-center justify-between px-4 text-white text-[10px] tracking-widest font-mono" style={{ backgroundColor: theme.primary }}>
              <span>KOMOREBI LOG JOURNAL</span>
              <span>2026 SPECIAL</span>
            </div>

            {/* 手帳頂部抬頭 */}
            <header className="px-6 pt-5 pb-3 border-b border-dashed" style={{ borderColor: theme.borderColor }}>
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-[10px] tracking-widest font-bold uppercase opacity-80" style={{ color: theme.primary }}>{theme.name}</p>
                  <h1 className="text-2xl font-black tracking-tight flex items-center gap-1.5 mt-0.5">Komorebi Log <span className="text-lg">🌿</span></h1>
                </div>

                <div className="flex items-center gap-2">
                  <button onClick={() => drawFortune(false)} className="px-2.5 py-1.5 rounded-full border border-dashed text-xs flex items-center gap-1 font-bold shadow-sm active:scale-95 transition-all" style={{ backgroundColor: theme.card, borderColor: theme.secondary, color: theme.secondary }}>
                    🏮 抽健康籤
                  </button>
                  <div className="flex gap-1 bg-stone-200/40 p-1 rounded-full">
                    {Object.keys(THEMES).map(k => (
                      <button key={k} onClick={() => setCurrentThemeKey(k)} className={`w-5 h-5 rounded-full border-2 transition-transform ${currentThemeKey === k ? 'scale-110 border-stone-600' : 'border-transparent'}`} style={{ backgroundColor: THEMES[k].primary }} />
                    ))}
                  </div>
                </div>
              </div>

              {/* 橫向星期標籤 */}
              <div className="flex justify-between gap-1 mt-5 overflow-x-auto pb-1 scrollbar-none">
                {Object.keys(dayNameMapping).map((day) => {
                  const isSelected = selectedDay === day;
                  return (
                    <button key={day} onClick={() => setSelectedDay(day)} className="flex-1 py-1.5 rounded-2xl text-center relative transition-all active:scale-95" style={{ minWidth: '46px', backgroundColor: isSelected ? theme.primary : theme.card, color: isSelected ? '#ffffff' : theme.neutral }}>
                      <p className="text-[9px] opacity-70 uppercase">{day}</p>
                      <p className="text-xs font-bold mt-0.5">{dayNameMapping[day].short}</p>
                      {stampedDays[day] && <span className="absolute -top-1 -right-1 text-[10px]">💮</span>}
                      {(placedStickers[day] || []).length > 0 && !stampedDays[day] && <span className="absolute top-1.5 right-1.5 w-1 h-1 rounded-full bg-red-400" />}
                    </button>
                  );
                })}
              </div>
            </header>

            {/* 主要內容區 */}
            <main className="flex-1 p-5 overflow-y-auto space-y-6 pb-28">
              {/* 子導覽頁籤 */}
              <div className="grid grid-cols-4 gap-1 p-1 rounded-2xl" style={{ backgroundColor: theme.card }}>
                {[
                  { id: 'diary', label: '今日日誌', icon: '🗒️' },
                  { id: 'planner', label: '健身計劃', icon: '📅' },
                  { id: 'library', label: '姿勢百科', icon: '📖' },
                  { id: 'garden', label: '嫩芽花園', icon: '🌱' },
                ].map(tab => (
                  <button key={tab.id} onClick={() => setActiveTab(tab.id)} className="py-2 text-[10px] font-bold rounded-xl flex flex-col items-center justify-center gap-0.5 transition-all" style={{ backgroundColor: activeTab === tab.id ? '#FAF6F0' : 'transparent', color: theme.neutral }}>
                    <span>{tab.icon}</span>
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* TAB 1: 今日日誌 */}
              {activeTab === 'diary' && (
                <div className="space-y-6">
                  <div className="p-5 rounded-3xl border relative shadow-sm" style={{ backgroundColor: theme.card, borderColor: theme.borderColor }}>
                    <div className="absolute -top-2.5 left-4 text-[9px] font-bold px-3 py-0.5 rounded-md text-white shadow-sm" style={{ backgroundColor: theme.secondary }}>DIET JOURNAL</div>
                    <div className="flex justify-between items-center mt-1 mb-4">
                      <h3 className="font-extrabold text-sm">{dayNameMapping[selectedDay].long} 目標進度</h3>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border bg-[#FAF6F0]" style={{ borderColor: theme.borderColor }}>1200 kcal / 80g 蛋白</span>
                    </div>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between text-xs font-bold mb-1"><span>🔥 熱量攝取</span><span>{totalCalories} / {CALORIE_LIMIT} kcal</span></div>
                        <div className="w-full bg-[#FAF6F0] h-3.5 rounded-full p-0.5 border" style={{ borderColor: theme.borderColor }}>
                          <div className="h-full rounded-full transition-all duration-500" style={{ width: `${Math.min((totalCalories / CALORIE_LIMIT) * 100, 100)}%`, backgroundColor: theme.secondary }} />
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-xs font-bold mb-1"><span>🌾 蛋白質補充</span><span>{totalProtein} / {PROTEIN_LIMIT} g</span></div>
                        <div className="w-full bg-[#FAF6F0] h-3.5 rounded-full p-0.5 border" style={{ borderColor: theme.borderColor }}>
                          <div className="h-full rounded-full transition-all duration-500" style={{ width: `${Math.min((totalProtein / PROTEIN_LIMIT) * 100, 100)}%`, backgroundColor: theme.primary }} />
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* AI 飲食輸入罐 */}
                  <div className="p-5 rounded-3xl border bg-[#FAF6F0] relative" style={{ borderColor: theme.borderColor }}>
                    <h3 className="font-extrabold text-sm flex items-center gap-1.5 text-stone-700">✨ AI 魔法飲食手札</h3>
                    <p className="text-[10px] text-stone-500 mt-1 leading-relaxed">輸入你吃了什麼，AI 將自動預估並記錄熱量與蛋白質！</p>
                    <form onSubmit={handleAiInputSubmit} className="mt-4 space-y-3">
                      <textarea placeholder="請描述您吃的食物... (例如: 吃了一塊雞胸肉跟茶葉蛋)" value={aiInputText} onChange={(e) => setAiInputText(e.target.value)} rows="2" className="w-full text-xs p-3 rounded-2xl bg-white border outline-none" style={{ borderColor: theme.borderColor }} />
                      <button type="submit" disabled={aiLoading} className="w-full py-2 rounded-xl text-xs font-bold text-white shadow-sm bg-stone-700 disabled:opacity-50" style={{ backgroundColor: theme.primary }}>
                        {aiLoading ? "召喚 AI 魔法中..." : "魔法解析並寫入手札"}
                      </button>
                    </form>
                  </div>

                  {/* 飲食細項 */}
                  <div className="border rounded-3xl p-5 bg-white/70" style={{ borderColor: theme.borderColor, backgroundImage: 'radial-gradient(#E8E1D5 1.2px, transparent 1.2px)', backgroundSize: '16px 16px' }}>
                    <h3 className="font-extrabold text-sm border-b-2 pb-0.5 mb-4" style={{ borderColor: theme.primary }}>🗒️ 今日飲食細項</h3>
                    {currentDayMeals.length === 0 ? (
                      <p className="py-4 text-center text-xs text-stone-400">目前空空如也，快用上方 AI 或手動記錄吧 🥐</p>
                    ) : (
                      <div className="space-y-2">
                        {currentDayMeals.map(meal => (
                          <div key={meal.id} className="flex items-center justify-between bg-white p-3 rounded-2xl border" style={{ borderColor: theme.borderColor }}>
                            <div className="min-w-0">
                              <p className="text-xs font-bold text-stone-700 truncate">{meal.name}</p>
                              <p className="text-[10px] text-stone-500">熱量: <span style={{ color: theme.secondary }}>{meal.calories} kcal</span> ｜ 蛋白: <span style={{ color: theme.primary }}>{meal.protein} g</span></p>
                            </div>
                            <button onClick={() => handleDeleteMeal(meal.id)} className="text-stone-400 hover:text-red-400 text-xs">❌</button>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* 手動輸入表單 */}
                    <form onSubmit={handleAddMeal} className="mt-5 pt-4 border-t border-dashed border-stone-300 space-y-2">
                      <input type="text" placeholder="手動新增食物名稱..." value={newMealName} onChange={e => setNewMealName(e.target.value)} className="w-full text-xs bg-white border rounded-xl px-3 py-2 outline-none" style={{ borderColor: theme.borderColor }} />
                      <div className="grid grid-cols-2 gap-2">
                        <input type="number" placeholder="卡路里 (kcal)" value={newMealCalories} onChange={e => setNewMealCalories(e.target.value)} className="w-full text-xs bg-white border rounded-xl px-3 py-2 outline-none" style={{ borderColor: theme.borderColor }} />
                        <input type="number" placeholder="蛋白質 (g)" value={newMealProtein} onChange={e => setNewMealProtein(e.target.value)} className="w-full text-xs bg-white border rounded-xl px-3 py-2 outline-none" style={{ borderColor: theme.borderColor }} />
                      </div>
                      <button type="submit" className="w-full py-2 text-white text-xs font-bold rounded-xl" style={{ backgroundColor: theme.primary }}>➕ 記錄此餐</button>
                    </form>
                  </div>

                  {/* 水分追蹤與貼紙 */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 rounded-3xl border bg-white/50 flex flex-col justify-between" style={{ borderColor: theme.borderColor }}>
                      <h4 className="font-extrabold text-xs text-stone-700">🍵 每日水分補給</h4>
                      <div className="my-3 flex flex-wrap gap-1 justify-center">
                        {[...Array(8)].map((_, i) => (
                          <span key={i} style={{ opacity: i < (waterCups[selectedDay] || 0) ? 1 : 0.2 }}>🍵</span>
                        ))}
                      </div>
                      <button onClick={handleDrinkWater} className="w-full py-1.5 rounded-xl text-[10px] font-bold text-white" style={{ backgroundColor: theme.primary }}>喝杯茶</button>
                    </div>

                    <div className="p-4 rounded-3xl border bg-white/50 flex flex-col justify-between" style={{ borderColor: theme.borderColor }}>
                      <h4 className="font-extrabold text-xs text-stone-700">🎨 手札貼紙盒</h4>
                      <div className="min-h-[35px] border border-dashed rounded-xl p-1 my-2 flex flex-wrap gap-1 bg-stone-50">
                        {(placedStickers[selectedDay] || []).map(sticker => (
                          <button key={sticker} onClick={() => handleRemoveSticker(sticker)} className="text-xs">
                            {sticker}
                          </button>
                        ))}
                      </div>
                      <div className="flex gap-1 overflow-x-auto pb-1 scrollbar-none">
                        {availableStickers.map(s => <button key={s} onClick={() => handleApplySticker(s)} className="text-xs">{s}</button>)}
                      </div>
                    </div>
                  </div>

                  {/* 智能推薦 */}
                  <div className="p-4 rounded-3xl border border-dashed text-left" style={{ borderColor: theme.secondary, backgroundColor: theme.card }}>
                    <h4 className="font-extrabold text-xs" style={{ color: theme.secondary }}>🌻 智能健康手札推薦</h4>
                    <p className="text-[10px] text-stone-600 mt-1 italic">"{feedback.text}"</p>
                    <div className="mt-3 space-y-2">
                      {recommendations.map((rec, i) => (
                        <div key={i} className="flex justify-between items-center bg-white/70 p-2 rounded-xl text-[10px]">
                          <div><span className="font-bold text-stone-700">{rec.name}</span></div>
                          <span className="font-bold px-2 py-0.5 rounded-full bg-stone-100">{rec.kcal} kcal</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="text-center"><button onClick={handleStampCheckin} className="px-6 py-3 rounded-full text-xs font-bold text-white shadow-md" style={{ backgroundColor: theme.secondary }}>💮 結算今日手帳並蓋章</button></div>
                </div>
              )}

              {/* TAB 2: 健身計劃 */}
              {activeTab === 'planner' && (
                <div className="space-y-6">
                  {/* 木質番茄休息計時器 */}
                  <div className="p-5 rounded-3xl border text-center shadow-sm relative" style={{ backgroundColor: theme.card, borderColor: theme.borderColor }}>
                    <h3 className="font-extrabold text-xs text-stone-700 mb-2">⏱️ 復古發條休息計時器</h3>
                    <div className="flex flex-col items-center justify-center gap-2">
                      <div className="w-24 h-24 rounded-full border-4 flex flex-col items-center justify-center bg-white shadow-inner" style={{ borderColor: theme.primary }}>
                        <span className="text-2xl font-black" style={{ color: theme.primary }}>{timerSeconds}s</span>
                      </div>
                      <div className="flex gap-1.5 my-2">
                        {[30, 60, 90].map(s => (
                          <button key={s} onClick={() => { setTimerPreset(s); setTimerSeconds(s); setTimerActive(false); }} className="px-2 py-0.5 text-[10px] border rounded-full" style={{ backgroundColor: timerPreset === s ? theme.primary : '#fff', color: timerPreset === s ? '#fff' : '#000' }}>{s}秒</button>
                        ))}
                      </div>
                      <div className="flex gap-4">
                        <button onClick={() => setTimerActive(!timerActive)} className="px-4 py-1 text-xs text-white rounded-full" style={{ backgroundColor: theme.primary }}>{timerActive ? "暫停" : "開始"}</button>
                        <button onClick={() => { setTimerActive(false); setTimerSeconds(timerPreset); }} className="px-4 py-1 text-xs bg-stone-300 rounded-full">重置</button>
                      </div>
                    </div>
                  </div>

                  {/* 週排程表 */}
                  <div className="p-5 rounded-3xl border bg-white/60 shadow-sm" style={{ borderColor: theme.borderColor }}>
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="font-extrabold text-sm text-stone-700">📅 本週健體排程</h3>
                      <button onClick={() => setShowCustomExModal(true)} className="px-2 py-1 text-[10px] bg-stone-100 rounded-lg">➕ 自訂動作</button>
                    </div>
                    <div className="space-y-3">
                      {Object.keys(dayNameMapping).map((dayKey) => {
                        const workoutIds = weeklyWorkouts[dayKey] || [];
                        const isSelected = selectedDay === dayKey;
                        return (
                          <div key={dayKey} onDragOver={handleDragOver} onDrop={(e) => handleDrop(e, dayKey)} onClick={() => setSelectedDay(dayKey)} className="p-3 rounded-2xl border cursor-pointer" style={{ backgroundColor: isSelected ? '#FAF6F0' : 'rgba(255,255,255,0.4)', borderColor: isSelected ? theme.primary : theme.borderColor, borderWidth: isSelected ? '2px' : '1px', borderStyle: isSelected ? 'dashed' : 'solid' }}>
                            <div className="flex justify-between text-xs font-bold mb-1">
                              <span>{dayNameMapping[dayKey].long}</span>
                              <span className="text-[10px] text-stone-400">{workoutIds.length} 個動作</span>
                            </div>
                            <div className="flex flex-wrap gap-1">
                              {workoutIds.map(id => {
                                const ex = exercisesDatabase.find(e => e.id === id);
                                if (!ex) return null;
                                return (
                                  <span key={id} className="text-[10px] px-2 py-0.5 rounded-full bg-white border flex items-center gap-1" style={{ color: theme.primary }}>
                                    {ex.name.split(' (')[0]}
                                    <button onClick={(e) => { e.stopPropagation(); removeExerciseFromDay(id, dayKey); }} className="text-red-500">×</button>
                                  </span>
                                );
                              })}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 3: 姿勢百科 */}
              {activeTab === 'library' && (
                <div className="space-y-3">
                  {exercisesDatabase.map(ex => (
                    <div key={ex.id} draggable onDragStart={(e) => handleDragStart(e, ex.id)} onClick={() => setActiveExerciseDetail(ex)} className="p-4 bg-white border rounded-3xl flex gap-3 cursor-pointer shadow-sm" style={{ borderColor: theme.borderColor }}>
                      <div className="p-2 bg-stone-50 rounded-2xl">{ex.svgPath(theme.primary)}</div>
                      <div className="flex-1">
                        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full" style={{ backgroundColor: theme.accentBg, color: theme.primary }}>{ex.category}</span>
                        <h4 className="font-extrabold text-xs mt-1 text-stone-700">{ex.name}</h4>
                        <p className="text-[10px] text-stone-500 line-clamp-1 mt-0.5">{ex.description}</p>
                        <div className="flex justify-between items-center mt-2 pt-2 border-t border-dashed">
                          <span className="text-[9px] text-stone-400">💡 點擊查看精緻呼吸指導</span>
                          <button onClick={(e) => { e.stopPropagation(); setAssigningExercise(ex); }} className="px-2 py-0.5 text-[9px] text-white rounded-md" style={{ backgroundColor: theme.primary }}>指派日程</button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* TAB 4: 嫩芽花園 */}
              {activeTab === 'garden' && (
                <div className="space-y-6">
                  <div className="p-6 rounded-3xl border text-center bg-white/80" style={{ borderColor: theme.borderColor }}>
                    <h3 className="font-extrabold text-sm text-stone-700">🌱 療癒嫩芽小精靈</h3>
                    <div className="flex justify-center items-center gap-1 mt-1">
                      {isEditingPetName ? (
                        <div>
                          <input type="text" value={petName} onChange={(e) => setPetName(e.target.value)} className="text-xs border px-2 py-0.5 rounded-lg text-center" />
                          <button onClick={() => setIsEditingPetName(false)} className="text-xs text-green-600 font-bold ml-1">確認</button>
                        </div>
                      ) : (
                        <div>
                          <span className="text-xs font-bold">「 {petName} 」</span>
                          <button onClick={() => setIsEditingPetName(true)} className="text-[10px] text-stone-400">🖋️ 改名</button>
                        </div>
                      )}
                    </div>

                    {/* 寵物進化盆栽動畫 */}
                    <div className="my-6 flex justify-center">
                      <div className="w-32 h-32 rounded-full bg-stone-50 border flex items-center justify-center relative shadow-inner">
                        <svg viewBox="0 0 100 100" className="w-24 h-24">
                          <path d="M30 75 H70 L65 90 H35 Z" fill="#8B5A2B" stroke="#4E423E" strokeWidth="2" />
                          <rect x="25" y="70" width="50" height="5" rx="2.5" fill="#CD853F" stroke="#4E423E" strokeWidth="2" />
                          {petStage === 1 && (
                            <g>
                              <circle cx="50" cy="65" r="4" fill="#CD853F" />
                              <path d="M50 65 Q52 55 55 52" stroke="#8C9E86" strokeWidth="3" fill="none" />
                            </g>
                          )}
                          {petStage === 2 && (
                            <g className="animate-bounce">
                              <path d="M50 70 Q50 50 45 42" stroke="#8C9E86" strokeWidth="4" fill="none" />
                              <path d="M45 42 Q35 40 38 48 Z" fill="#8C9E86" />
                            </g>
                          )}
                          {petStage === 3 && (
                            <g>
                              <path d="M50 70 Q50 45 48 35" stroke="#8C9E86" strokeWidth="4" fill="none" />
                              <ellipse cx="48" cy="30" rx="6" ry="8" fill="#E09F9E" />
                            </g>
                          )}
                          {petStage === 4 && (
                            <g className="animate-pulse">
                              <path d="M50 70 L50 35" stroke="#8C9E86" strokeWidth="4" />
                              <circle cx="50" cy="35" r="12" fill="#E09F9E" />
                              <circle cx="50" cy="35" r="5" fill="#DFB15B" />
                            </g>
                          )}
                        </svg>
                        <div className="absolute -bottom-2 bg-white px-2 py-0.5 text-[9px] font-bold border rounded-md">等級 {petStage} 🌸</div>
                      </div>
                    </div>

                    <div className="space-y-1 text-left mt-4">
                      <div className="flex justify-between text-[10px] font-bold"><span>🌱 成長養分進度</span><span>{petExp} / 100 EXP</span></div>
                      <div className="w-full bg-stone-100 h-2 rounded-full overflow-hidden border"><div className="h-full bg-green-400" style={{ width: `${petExp}%` }} /></div>
                      <p className="text-[10px] text-stone-400 text-center italic mt-2">"{petActionMessage}"</p>
                    </div>
                  </div>

                  {/* 特製打卡蓋章牆 */}
                  <div className="p-5 rounded-3xl border bg-white/50" style={{ borderColor: theme.borderColor }}>
                    <h3 className="font-extrabold text-sm mb-1">💮 本月合格印章牆</h3>
                    <div className="grid grid-cols-7 gap-1 text-center mt-3">
                      {Object.keys(dayNameMapping).map(dayKey => (
                        <div key={dayKey} className="p-1 border border-dashed rounded-xl bg-white/80">
                          <p className="text-[8px] text-stone-400">{dayNameMapping[dayKey].short}</p>
                          <div className="w-7 h-7 mx-auto rounded-full flex items-center justify-center text-xs bg-stone-50 mt-1">
                            {stampedDays[dayKey] ? "💮" : "•"}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </main>

            {/* 御神籤彈出視窗 */}
            {showFortuneModal && drawnFortune && (
              <div className="fixed inset-0 bg-stone-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-6">
                <div className="bg-[#FAF6F0] w-full max-w-xs rounded-3xl border-2 border-red-400 p-6 shadow-2xl text-center relative">
                  <button onClick={() => setShowFortuneModal(false)} className="absolute top-3 right-3 text-stone-400 text-sm">❌</button>
                  <h2 className="text-xl font-black text-red-500">{drawnFortune.rank}</h2>
                  <h3 className="font-extrabold text-sm text-stone-700 mt-2">{drawnFortune.title}</h3>
                  <div className="bg-white border p-4 rounded-2xl my-4 text-xs text-stone-600 text-left border-dashed" style={{ borderColor: theme.borderColor }}>{drawnFortune.tip}</div>
                  <div className="space-y-2">
                    <button onClick={() => drawFortune(true)} className="w-full py-2 bg-stone-200 rounded-xl text-xs font-bold">🔄 重新求一籤</button>
                    <button onClick={() => setShowFortuneModal(false)} className="w-full py-2 bg-red-400 text-white rounded-xl text-xs font-bold">收下祝福</button>
                  </div>
                </div>
              </div>
            )}

            {/* 健身動作細節彈出視窗 */}
            {activeExerciseDetail && (
              <div className="fixed inset-0 bg-stone-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-6">
                <div className="bg-[#FAF6F0] w-full max-w-sm rounded-3xl border-2 p-6 shadow-2xl relative" style={{ borderColor: theme.primary }}>
                  <button onClick={() => setActiveExerciseDetail(null)} className="absolute top-4 right-4 text-stone-500">❌</button>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-stone-100">{activeExerciseDetail.category}</span>
                  <h3 className="text-base font-extrabold text-stone-700 mt-1">{activeExerciseDetail.name}</h3>
                  <div className="bg-white p-4 rounded-2xl border flex justify-center my-3" style={{ borderColor: theme.borderColor }}>{activeExerciseDetail.svgPath(theme.primary)}</div>
                  <div className="space-y-2 text-xs text-stone-600">
                    <p><strong>📖 動作詳解：</strong>{activeExerciseDetail.description}</p>
                    <p><strong>💡 貼士提示：</strong>{activeExerciseDetail.tips}</p>
                    <p><strong>💨 呼吸指導：</strong>{activeExerciseDetail.breathing}</p>
                  </div>
                  <button onClick={() => { setAssigningExercise(activeExerciseDetail); setActiveExerciseDetail(null); }} className="w-full mt-4 py-2 text-white text-xs font-bold rounded-xl" style={{ backgroundColor: theme.primary }}>將動作編排進日程</button>
                </div>
              </div>
            )}

            {/* 自定義動作彈窗 */}
            {showCustomExModal && (
              <div className="fixed inset-0 bg-stone-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-6">
                <div className="bg-[#FAF6F0] w-full max-w-sm rounded-3xl border-2 p-5 shadow-2xl relative" style={{ borderColor: theme.primary }}>
                  <button onClick={() => setShowCustomExModal(false)} className="absolute top-4 right-4 text-stone-400">❌</button>
                  <h4 className="font-extrabold text-sm mb-4">🎨 創作您專屬的健身動作卡片</h4>
                  <form onSubmit={handleAddCustomExercise} className="space-y-3">
                    <input type="text" required placeholder="動作名稱..." value={customExName} onChange={(e) => setCustomExName(e.target.value)} className="w-full text-xs border rounded-xl px-3 py-2 outline-none" />
                    <textarea placeholder="動作貼士與小提示..." value={customExTips} onChange={(e) => setCustomExTips(e.target.value)} className="w-full text-xs border rounded-xl p-3 outline-none" rows="2" />
                    <button type="submit" className="w-full py-2 text-white rounded-xl text-xs font-bold" style={{ backgroundColor: theme.primary }}>確認創立專屬姿勢卡</button>
                  </form>
                </div>
              </div>
            )}

            {/* 指派日程彈窗 */}
            {assigningExercise && (
              <div className="fixed inset-0 bg-stone-900/60 backdrop-blur-xs flex items-center justify-center z-50 p-6">
                <div className="bg-[#FAF6F0] w-full max-w-xs rounded-3xl border-2 p-5 shadow-2xl relative" style={{ borderColor: theme.secondary }}>
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-bold text-xs text-stone-700">選擇排程星期</h4>
                    <button onClick={() => setAssigningExercise(null)} className="text-stone-400">❌</button>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.keys(dayNameMapping).map(dayKey => (
                      <button key={dayKey} onClick={() => { addExerciseToDay(assigningExercise.id, dayKey); setAssigningExercise(null); setActiveTab('planner'); }} className="py-2 px-3 rounded-xl text-[10px] font-bold bg-white border text-left flex justify-between items-center" style={{ borderColor: theme.borderColor }}>
                        <span>{dayNameMapping[dayKey].long}</span> ➔
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* 蓋章成功通知浮層 */}
            {showStampSuccess && (
              <div className="absolute inset-x-0 top-1/3 flex justify-center items-center z-50 pointer-events-none">
                <div className="bg-white/95 p-6 rounded-3xl border-2 border-red-400 shadow-2xl flex flex-col items-center gap-2 animate-bounce">
                  <span className="text-5xl">💮</span>
                  <h4 className="font-black text-red-500">本日手札結算完成！</h4>
                  <p className="text-[10px] text-stone-500">嫩芽也開心地長大了唷！</p>
                </div>
              </div>
            )}

            {/* 底部導覽列 */}
            <div className="absolute bottom-0 inset-x-0 bg-white border-t py-2 px-6 flex justify-around items-center text-stone-400 shadow-2xl z-40" style={{ borderColor: theme.borderColor }}>
              <button onClick={() => setActiveTab('diary')} className="flex flex-col items-center text-[10px] font-extrabold" style={{ color: activeTab === 'diary' ? theme.primary : undefined }}>
                <span>🗒️</span>今日日誌
              </button>
              <div className="relative -top-4">
                <button onClick={() => setActiveTab('planner')} className="w-11 h-11 text-white rounded-full flex items-center justify-center shadow-lg" style={{ backgroundColor: theme.primary }}>🏋️</button>
              </div>
              <button onClick={() => setActiveTab('library')} className="flex flex-col items-center text-[10px] font-extrabold" style={{ color: activeTab === 'library' ? theme.primary : undefined }}>
                <span>📖</span>姿勢百科
              </button>
            </div>

          </div>
        </div>
      );
    }

    const root = tragedies = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
