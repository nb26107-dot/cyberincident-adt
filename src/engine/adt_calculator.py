def calculate_inhibition_node(
        self, 
        attack_interval: Tuple[float, float], 
        defense_efficiency: float,
        attacker_cost: float,
        defender_cost: float
    ) -> Dict[str, any]:
        """
        Gerbang Inhibition: Menjembatani serangan dengan pertahanan sekaligus 
        menghitung dampak biaya (Cost Imposing) bagi kedua belah pihak.
        
        Args:
            attack_interval: Rentang probabilitas serangan (min, max).
            defense_efficiency: Tingkat efektivitas pertahanan (0.0 - 1.0).
            attacker_cost: Biaya/sumber daya yang harus dikeluarkan penyerang jika menembus titik ini.
            defender_cost: Biaya implementasi kontrol pertahanan oleh pemilik sistem.
            
        Returns:
            Dict berisi sisa probabilitas serangan, biaya, dan rasio efisiensi biaya.
        """
        # 1. Hitung sisa probabilitas setelah diinhibisi (dihambat) oleh defense
        inhibited_interval = self.apply_defense_mitigation(attack_interval, defense_efficiency)
        
        # 2. Hitung Return on Investment (ROI) Keamanan atau Rasio Efisiensi Biaya
        # Formula: Berapa besar penurunan risiko maksimal per satuan biaya yang dikeluarkan defender
        risk_reduction = attack_interval[1] - inhibited_interval[1]
        
        cost_efficiency_ratio = 0.0
        if defender_cost > 0:
            # Dikalikan 1000 hanya untuk penskalaan indeks agar mudah dibaca pemilik sistem
            cost_efficiency_ratio = round((risk_reduction / defender_cost) * 1000, 4)
            
        # 3. Rekomendasi Prioritas berdasarkan Cost Imposing Attacker vs Defender
        # Jika biaya penyerang sangat tinggi dan biaya pertahanan murah -> Titik Kritikal Utama (Quick Win)
        is_critical_leverage_point = (attacker_cost > defender_cost * 2) and (defense_efficiency >= 0.5)

        return {
            "residual_probability": inhibited_interval,
            "attacker_cost": attacker_cost,
            "defender_cost": defender_cost,
            "cost_efficiency_ratio": cost_efficiency_ratio,
            "is_critical_point": is_critical_leverage_point,
            "recommendation_priority": "HIGH" if is_critical_leverage_point else "MEDIUM" if defense_efficiency > 0 else "LOW"
        }
