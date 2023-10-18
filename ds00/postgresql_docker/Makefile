# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    Makefile                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/18 17:53:24 by cmariot          #+#    #+#              #
#    Updated: 2023/10/18 17:53:25 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

up:
	bash ./create_env.sh
	docker compose up

stop:
	docker compose stop

list:
	docker compose ps -a

clean:
	docker compose down --rmi all --volumes --remove-orphans

fclean: clean
	rm -rf ./postgres_data

re: fclean up

db-shell:
	docker compose exec postgres bash

.PHONY: up stop list clean fclean db-shell