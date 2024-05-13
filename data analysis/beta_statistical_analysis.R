# Marcin J. Marzejon, May 2024
vis_beta_P1 <- c(16.9317, 12.0115, 13.6162, 18.4521, 16.3095, 21.7461, 21.7170, 
                 18.8365, 30.5492, 17.0039, 18.7317, 16.0615)
ir_beta_P1 <- c(36.4178, 37.1673, 25.6775, 34.0700, 31.6388, 23.4112, 36.9355, 
               38.7069, 31.6107, 23.9046, 43.5405)
vis_beta_P26 <- c(29.9098, 20.3406, 25.9845, 16.7547)
ir_beta_P26 <- c(15.2449, 24.3758, 33.9389, 47.6362, 32.3291)
vis_beta_P36 <- c(17.2640, 19.0161, 21.2769, 25.4831, 12.9846, 18.6112, 18.6153)
ir_beta_P36 <- c(26.1592, 31.1328, 32.9899, 22.1169, 23.2335, 33.3988)

vis_beta <- c(vis_beta_P1, vis_beta_P26, vis_beta_P36)
ir_beta <- c(ir_beta_P1, ir_beta_P26, ir_beta_P36)

library(outliers)

# tests for outliners - vis
outliers_vis <- dixon.test(vis_beta, opposite = T)
print(outliers_vis)
outliers_vis <- dixon.test(vis_beta, opposite = F)
print(outliers_vis)
# tests for outliners - ir
outliers_ir <- dixon.test(ir_beta, opposite = T)
print(outliers_ir)
outliers_ir <- dixon.test(ir_beta, opposite = F)
print(outliers_ir)

# normality tests - vis
norm_vis <- shapiro.test(vis_beta)
print(norm_vis)
# normality tests - ir
norm_ir <- shapiro.test(ir_beta)
print(norm_ir)

# test for equal variance
bartlett.test(c(vis_beta, ir_beta), c(rep(1, length(vis_beta)), rep(2, length(ir_beta))))

# test for equal mean values
tStudent <- t.test(vis_beta, ir_beta, alternative = "two.sided", var.equal = F)
print(tStudent)
