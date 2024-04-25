import numpy as np

# 広告効果を推定する関数
def estimate_effect(ad_features, user_profile):
    # 線形モデルを仮定
    effect = np.dot(ad_features, user_profile)
    return effect

# 広告コストを計算する関数
def calculate_cost(impressions, cpc):
    cost = impressions * cpc
    return cost

# 広告コストを計算する関数
def knapsack_dp(ad_options, budget, user_profile):
    n = len(ad_options)  # 広告オプションの数
    # DPテーブルを初期化
    dp = np.zeros((n+1, budget+1))
    
    for i in range(1, n+1):
        ad_features, impressions, cpc = ad_options[i-1]
        cost = calculate_cost(impressions, cpc)
        effect = estimate_effect(ad_features, user_profile)
        
        for w in range(budget+1):
            if cost <= w:  # この広告を選択できる場合
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-int(cost)] + effect)
            else:
                dp[i][w] = dp[i-1][w]
    
    # 最適な広告の組み合わせを復元
    w = budget
    selected_ads = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            ad_features, impressions, cpc = ad_options[i-1]
            selected_ads.append((ad_features, impressions, cpc))
            w -= int(calculate_cost(impressions, cpc))
    
    selected_ads.reverse()
    total_effect = dp[n][budget]
    return selected_ads, total_effect

# サンプルデータ
ad_features1 = np.array([0.3, 0.5])
ad_features2 = np.array([0.4, 0.1])
ad_features3 = np.array([0.5, 0.6])
ad_features4 = np.array([0.2, 0.3])

user_profiles = [
    np.array([0.6, 0.4]),
    np.array([0.2, 0.8]),
    np.array([0.5, 0.5])
]

impressions1 = 1000
impressions2 = 1500
impressions3 = 500

cpc1 = 0.05
cpc2 = 0.08
cpc3 = 0.10

budget = 100

ad_options = [
    (ad_features1, impressions1, cpc1),
    (ad_features1, impressions2, cpc3),
    (ad_features2, impressions1, cpc2),
    (ad_features2, impressions3, cpc3),
    (ad_features3, impressions2, cpc1),
    (ad_features4, impressions3, cpc2)
]

# 各ユーザープロファイルに対して最適化を実行し、結果を表示
for i, user_profile in enumerate(user_profiles, 1):
    selected_ads, total_cost = selected_ads, total_effect = knapsack_dp(ad_options, budget, user_profile)
    print(f"ユーザープロファイル {i} の結果:")
    for ad in selected_ads:
        print(f"  広告特性: {ad[0]}, 表示回数: {ad[1]}, CPC: {ad[2]}")
    print(f"  総コスト: {total_cost}\n")