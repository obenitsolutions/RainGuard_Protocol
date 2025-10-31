// RainGuard Protocol - Vue.js Application Logic
const { createApp } = Vue;

createApp({
    data() {
        return {
            ws: null,
            systemStatus: {
                text: 'Connecting...',
                class: 'connecting'
            },
            stats: {
                total_farmers: 0,
                total_regions: 8,
                active_claims: 0,
                total_disbursed: 0
            },
            weatherUpdates: [],
            verifications: [],
            activeClaims: [],
            disbursements: [],
            emails: [],
            aiAnalyses: [],
            activityLog: [],
            claimsMap: {},
            weatherCount: 0,
            totalClaims: 0,
            totalDisbursed: 0,
            completedClaims: 0
        };
    },

    mounted() {
        this.connectWebSocket();
        this.loadInitialData();
    },

    methods: {
        connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.systemStatus = {
                    text: 'Live',
                    class: 'online'
                };
                this.addActivityLog('System Connected', 'System is now live and monitoring data', 'success');
            };
            
            this.ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                this.handleMessage(message);
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.systemStatus = {
                    text: 'Error',
                    class: 'error'
                };
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.systemStatus = {
                    text: 'Disconnected',
                    class: 'disconnected'
                };
                // Attempt to reconnect after 3 seconds
                setTimeout(() => this.connectWebSocket(), 3000);
            };
            
            // Keep alive
            setInterval(() => {
                if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                    this.ws.send('ping');
                }
            }, 30000);
        },

        async loadInitialData() {
            try {
                const response = await axios.get('/api/stats');
                this.stats = response.data;
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        },

        handleMessage(message) {
            const { type, data } = message;
            
            switch (type) {
                case 'system_ready':
                    this.stats.total_farmers = data.registered_farmers;
                    this.stats.total_regions = data.regions;
                    this.addActivityLog('System Ready', data.message, 'success');
                    break;
                    
                case 'weather_update':
                    this.handleWeatherUpdate(data);
                    break;
                    
                case 'no_farmers':
                    this.addActivityLog('No Farmers', `No registered farmers in ${data.region}`, 'warning');
                    break;
                    
                case 'farmer_detected':
                    this.handleFarmerDetected(data);
                    break;
                    
                case 'blockchain_verification':
                    this.handleBlockchainVerification(data);
                    break;
                    
                case 'blockchain_verified':
                    this.handleBlockchainVerified(data);
                    break;
                    
                case 'payout_calculation':
                    this.handlePayoutCalculation(data);
                    break;
                    
                case 'preemptive_disbursement':
                    this.handleDisbursement(data, 'preemptive');
                    break;
                    
                case 'email_sent':
                    this.handleEmailSent(data);
                    break;
                    
                case 'photo_submission':
                    this.handlePhotoSubmission(data);
                    break;
                    
                case 'ai_analysis_started':
                    this.handleAIAnalysisStarted(data);
                    break;
                    
                case 'ai_analysis_completed':
                    this.handleAIAnalysisCompleted(data);
                    break;
                    
                case 'final_settlement':
                    this.handleDisbursement(data, 'final');
                    break;
                    
                case 'claim_completed':
                    this.handleClaimCompleted(data);
                    break;
            }
        },

        handleWeatherUpdate(data) {
            this.weatherUpdates.unshift(data);
            if (this.weatherUpdates.length > 20) {
                this.weatherUpdates = this.weatherUpdates.slice(0, 20);
            }
            this.weatherCount++;
            
            if (data.status === 'drought_detected') {
                this.addActivityLog(
                    'Drought Detected',
                    `High drought probability (${(data.drought_probability * 100).toFixed(1)}%) in ${data.region}`,
                    'danger'
                );
            }
        },

        handleFarmerDetected(data) {
            // Initialize claim tracking
            this.claimsMap[data.farmer_id] = {
                farmer_id: data.farmer_id,
                name: data.name,
                region: data.region,
                location: data.location,
                step: 1,
                payout_amount: null
            };
            
            this.activeClaims.unshift(this.claimsMap[data.farmer_id]);
            if (this.activeClaims.length > 10) {
                this.activeClaims = this.activeClaims.slice(0, 10);
            }
            
            this.totalClaims++;
            
            this.addActivityLog(
                'Farmer Detected',
                `${data.name} detected in affected area (${data.region})`,
                'info'
            );
        },

        handleBlockchainVerification(data) {
            const verification = {
                farmer_id: data.farmer_id,
                name: this.claimsMap[data.farmer_id]?.name || 'Unknown',
                wallet_address: data.wallet_address,
                contract_address: data.contract_address,
                status: data.status,
                timestamp: data.timestamp
            };
            
            this.verifications.unshift(verification);
            if (this.verifications.length > 10) {
                this.verifications = this.verifications.slice(0, 10);
            }
            
            if (this.claimsMap[data.farmer_id]) {
                this.claimsMap[data.farmer_id].step = 2;
            }
            
            this.addActivityLog(
                'Blockchain Verification',
                `Verifying ${verification.name} on Solana blockchain`,
                'info'
            );
        },

        handleBlockchainVerified(data) {
            // Update verification status
            const verification = this.verifications.find(v => v.farmer_id === data.farmer_id);
            if (verification) {
                verification.status = 'verified';
                verification.transaction_signature = data.transaction_signature;
            }
            
            if (this.claimsMap[data.farmer_id]) {
                this.claimsMap[data.farmer_id].step = 2;
            }
            
            this.addActivityLog(
                'Verification Success',
                `Blockchain verification completed successfully`,
                'success'
            );
        },

        handlePayoutCalculation(data) {
            if (this.claimsMap[data.farmer_id]) {
                this.claimsMap[data.farmer_id].step = 3;
                this.claimsMap[data.farmer_id].payout_amount = data.preemptive_payout;
            }
            
            this.addActivityLog(
                'Payout Calculated',
                `Pre-emptive payout: $${data.preemptive_payout} (${(data.drought_probability * 100).toFixed(1)}% drought probability)`,
                'info'
            );
        },

        handleDisbursement(data, type) {
            const disbursement = {
                ...data,
                type: type
            };
            
            this.disbursements.unshift(disbursement);
            if (this.disbursements.length > 10) {
                this.disbursements = this.disbursements.slice(0, 10);
            }
            
            if (this.claimsMap[data.farmer_id]) {
                this.claimsMap[data.farmer_id].step = 4;
            }
            
            this.totalDisbursed += data.amount;
            
            this.addActivityLog(
                type === 'preemptive' ? 'Pre-emptive Disbursement' : 'Final Settlement',
                `$${data.amount} sent to ${data.name}`,
                'success'
            );
        },

        handleEmailSent(data) {
            this.emails.unshift(data);
            if (this.emails.length > 10) {
                this.emails = this.emails.slice(0, 10);
            }
            
            this.addActivityLog(
                'Email Notification',
                `Email sent to ${data.email}`,
                'info'
            );
        },

        handlePhotoSubmission(data) {
            const analysis = {
                farmer_id: data.farmer_id,
                name: data.name,
                num_photos: data.num_photos,
                location: data.location,
                status: 'received',
                timestamp: data.timestamp
            };
            
            this.aiAnalyses.unshift(analysis);
            if (this.aiAnalyses.length > 10) {
                this.aiAnalyses = this.aiAnalyses.slice(0, 10);
            }
            
            this.addActivityLog(
                'Photos Received',
                `${data.name} submitted ${data.num_photos} crop photos`,
                'info'
            );
        },

        handleAIAnalysisStarted(data) {
            const analysis = this.aiAnalyses.find(a => a.farmer_id === data.farmer_id);
            if (analysis) {
                analysis.status = 'analyzing';
                analysis.model = data.model;
            }
            
            this.addActivityLog(
                'AI Analysis Started',
                `Running PlantVillage model analysis`,
                'info'
            );
        },

        handleAIAnalysisCompleted(data) {
            const analysis = this.aiAnalyses.find(a => a.farmer_id === data.farmer_id);
            if (analysis) {
                Object.assign(analysis, {
                    ...data,
                    status: 'completed'
                });
            }
            
            this.addActivityLog(
                'AI Analysis Complete',
                `Detected: ${data.health_classification} (${(data.confidence * 100).toFixed(1)}% confidence, ${data.yield_loss_percent}% yield loss)`,
                data.damage_verified ? 'success' : 'warning'
            );
        },

        handleClaimCompleted(data) {
            if (this.claimsMap[data.farmer_id]) {
                this.claimsMap[data.farmer_id].step = 5;
            }
            
            this.completedClaims++;
            
            this.addActivityLog(
                'Claim Completed',
                `Full claim processed for ${data.name} - Total: $${data.total_payout}`,
                'success'
            );
        },

        addActivityLog(title, message, type = 'info') {
            this.activityLog.unshift({
                title,
                message,
                type,
                timestamp: new Date().toISOString()
            });
            
            if (this.activityLog.length > 50) {
                this.activityLog = this.activityLog.slice(0, 50);
            }
        },

        formatTime(timestamp) {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = Math.floor((now - date) / 1000);
            
            if (diff < 60) return 'Just now';
            if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
            if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
            return date.toLocaleTimeString();
        },

        getDroughtClass(probability) {
            if (probability > 0.70) return 'high';
            if (probability > 0.40) return 'medium';
            return 'low';
        },

        getActivityIcon(type) {
            const icons = {
                success: 'fas fa-check-circle',
                warning: 'fas fa-exclamation-triangle',
                danger: 'fas fa-times-circle',
                info: 'fas fa-info-circle'
            };
            return icons[type] || 'fas fa-circle';
        }
    }
}).mount('#app');

