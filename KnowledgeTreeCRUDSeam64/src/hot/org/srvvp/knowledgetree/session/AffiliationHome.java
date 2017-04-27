package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("affiliationHome")
public class AffiliationHome extends EntityHome<Affiliation> {

	public void setAffiliationId(String id) {
		setId(id);
	}

	public String getAffiliationId() {
		return (String) getId();
	}

	@Override
	protected Affiliation createInstance() {
		Affiliation affiliation = new Affiliation();
		return affiliation;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public Affiliation getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<PersonHasAffiliation> getPersonHasAffiliations() {
		return getInstance() == null
				? null
				: new ArrayList<PersonHasAffiliation>(getInstance()
						.getPersonHasAffiliations());
	}

}
