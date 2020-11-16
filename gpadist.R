library(tidyverse)

x = rnorm(2581, mean = 3.07, sd = 0.2)
y = rnorm(5161, mean = 3.5, sd = 0.2)
z = rnorm(1290, mean = 2.5, sd = 0.2)
a = rnorm(645, mean = 2.75, sd = 0.2)
b = rnorm(323, mean = 2, sd = 0.2)


tibble = tibble(
  values = sample(c(x, y, z, a, b))
)

tibble = tibble %>% 
  mutate(values = as.numeric(values),
         values = if_else(values > 4.0, 4.0, values))

ggplot(data = tibble, aes(x = values)) +
  geom_histogram(color = "black") +
  geom_vline(xintercept = c(mean(tibble$values), 
                            median(tibble$values)),
             color = c("red", "orange"), lwd = 1.5)

mean(tibble$values) 
median(tibble$values)
min(tibble$values)
max(tibble$values)

write_csv(tibble, "gpadist.csv", col_names = FALSE)
