# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from examples.hello_world.run import run_hello_world

from conversationinsights.agent import Agent
from conversationinsights.channels import UserMessage
from conversationinsights.policies.scoring_policy import ScoringPolicy

import logging
logger = logging.getLogger(__name__)

logging.basicConfig(level="INFO")


def test_agent_train(tmpdir, default_domain):
    training_data_file = 'examples/concerts/data/stories.md'
    agent = Agent("examples/concerts/concert_domain.yml",
                  policies=[ScoringPolicy()])

    agent.train(training_data_file, max_history=3)
    agent.persist(tmpdir.strpath)
    logger.info("path:{}".format(tmpdir.strpath))
    loaded = Agent.load(tmpdir.strpath)
    # test featurizer
    assert type(loaded.featurizer) is type(agent.featurizer)    # nopep8

    # test domain
    assert [a.id_str() for a in loaded.domain.actions] == \
           [a.id_str() for a in agent.domain.actions]
    assert loaded.domain.intents == agent.domain.intents
    assert loaded.domain.entities == agent.domain.entities
    assert loaded.domain.templates == agent.domain.templates
    assert [s.name for s in loaded.domain.slots] == \
           [s.name for s in agent.domain.slots]

    # test policies
    assert type(loaded.policy_ensemble) is type(agent.policy_ensemble)  # nopep8
    assert [type(p) for p in loaded.policy_ensemble.policies] == \
           [type(p) for p in agent.policy_ensemble.policies]


def test_agent_handle_message():
    agent = run_hello_world(serve_forever=False)
    result = agent.handle_message("hello bot")
    assert result == ["你好！"]
