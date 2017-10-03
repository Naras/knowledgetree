package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("stateList")
public class StateList extends EntityQuery<State> {

	private static final String EJBQL = "select state from State state";

	private static final String[] RESTRICTIONS = {
			"lower(state.id.countryId) like lower(concat(#{stateList.state.id.countryId},'%'))",
			"lower(state.id.id) like lower(concat(#{stateList.state.id.id},'%'))",
			"lower(state.name) like lower(concat(#{stateList.state.name},'%'))",};

	private State state;

	public StateList() {
		state = new State();
		state.setId(new StateId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public State getState() {
		return state;
	}
}
